package hex.genmodel.algos.targetencoder;

import hex.ModelCategory;
import hex.genmodel.GenModel;
import hex.genmodel.MojoTransformer;
import hex.genmodel.easy.*;
import hex.genmodel.easy.exception.PredictException;

import java.util.*;

import static hex.genmodel.algos.targetencoder.TargetEncoderMojoModel.name2Idx;

class TargetEncoderAsModelProcessor implements MojoTransformer.DataTransformer {

    private final GenModel _model;
    private final TargetEncoderMojoModel _teModel;
    private final Map<String, Integer> _teColumnsToOffset = new HashMap<>();
    private final Map<Integer, CategoricalEncoder> _teOffsetToEncoder = new HashMap<>();
    private final Map<String, String[]> _columnsToDomainAfterTE = new LinkedHashMap<>(); //we need a guaranteed iteration order

    public TargetEncoderAsModelProcessor(TargetEncoderMojoModel teModel, GenModel model) {
        _teModel = teModel;
        _model = model;
        fillMaps();
    }

    @Override
    public RowToRawDataConverter makeRowConverter(EasyPredictModelWrapper.ErrorConsumer errorConsumer,
                                                  EasyPredictModelWrapper.Config config) {
        return new TargetEncoderRowToRawDataConverter(
                _teModel, 
                _teColumnsToOffset,
                _teOffsetToEncoder,
                errorConsumer,
                config
        );
    }

    @Override
    public GenModel getTransformedModel() {
        String[] newNames = _columnsToDomainAfterTE.keySet().toArray(new String[0]);
        String[][] newDomains = _columnsToDomainAfterTE.values().toArray(new String[0][]);
        return new VirtualTargetEncodedModel(_model, newNames, newDomains, _model.getResponseName());
    }

    private void fillMaps() {
        final String[] origNames = _model.getOrigNames();
        final String[][] origDomainValues = _model.getOrigDomainValues();
        final Map<String, Integer> nameToIdx = name2Idx(_model.getOrigNames());

        //trying to sort columns in the same way as in TargetEncoderModel#reorderColumns:
        // 1. non-categorical predictors
        // 2. TE-encoded predictors
        // 3. remaining categorical predictors are excluded (they will be encoded by the next preprocessor or categorical encoder)
        int offset = 0;
        final Set<Integer> catPredictors = new TreeSet<>();
        for (int i = 0; i < _model.getOrigNumCols(); i++) { //adding non-categoricals
            if (origDomainValues[i] != null) {
                catPredictors.add(i);
                continue;
            }
            if (_teModel._nonPredictors.contains(origNames[i])) continue; //non-predictors (fold, offset, weights...) are added to the end
            
//            _teColumnsToOffset.put(origNames[i], offset++);
            offset++;
            _columnsToDomainAfterTE.put(origNames[i], null);
        }
        for (ColumnsToSingleMapping columnsMapping : _teModel._inencMapping) {
            // the interaction column is generated by the TargetEncoderRowToRawDataConverter 
            //  so, we can focus here on the columns having an associated EncodingMap
            String[] colGroup = columnsMapping.from();
            String colToEncode = columnsMapping.toSingle(); 
            EncodingMap encodings = _teModel.getEncodings(columnsMapping.toSingle());
            
            _teColumnsToOffset.put(colToEncode, offset);
            String[] domain = colGroup.length > 1 ? columnsMapping.toDomain() : origDomainValues[nameToIdx.get(colGroup[0])];
            _teOffsetToEncoder.put(offset, new TargetEncoderAsCategoricalEncoder(_teModel, encodings, colToEncode, offset, domain));
            offset += _teModel.getNumEncColsPerPredictor();
            for (String teCol : findTEEncodedColumnsFor(colGroup)) {
                _columnsToDomainAfterTE.put(teCol, null);
            }
            if (!_teModel._keepOriginalCategoricalColumns) {
                for (String col: colGroup) {
                    Integer oriIdx = nameToIdx.get(col);
                    catPredictors.remove(oriIdx);
                }
            }
        }

        for (int idx : catPredictors) { //adding remaining categorical predictors
            _columnsToDomainAfterTE.put(origNames[idx], origDomainValues[idx]);
        }
        for (String col : _teModel._nonPredictors) {
            if (!col.equals(_teModel.getResponseName()))
                _columnsToDomainAfterTE.put(col, null);
        }
    }

    private String[] findTEEncodedColumnsFor(String[] columns) {
        for (ColumnsMapping colMapping : _teModel._inoutMapping) {
            if (Arrays.equals(columns, colMapping.from())) return colMapping.to();
        }
        return new String[0];
    }
    
    private static class TargetEncoderAsCategoricalEncoder implements CategoricalEncoder {
    
        private final TargetEncoderMojoModel _teModel;
        private final EncodingMap _encodings;
        private final String _columnName;
        private final int _offsetIndex;
        private final Map<String, Integer> _domainMap;
        
        public TargetEncoderAsCategoricalEncoder(TargetEncoderMojoModel teModel, 
                                                 EncodingMap encodings, String columnName, 
                                                 int offsetIndex, String[] domainValues) {
            _teModel = teModel;
            _encodings = encodings;
            _columnName = columnName;
            _offsetIndex = offsetIndex;
            _domainMap = new HashMap<>(domainValues.length);
            for (int j = 0; j < domainValues.length; j++) {
                _domainMap.put(domainValues[j], j);
            }
        }
    
        @Override
        public boolean encodeCatValue(String level, double[] rawData) {
            Integer category = _domainMap.get(level);
            if (category == null) return false;
            _teModel.encodeCategory(rawData, _offsetIndex, _encodings, category);
            return true;
        }
    
        @Override
        public void encodeNA(double[] rawData) {
            _teModel.encodeNA(rawData, _offsetIndex, _encodings, _columnName);
        }
        
    }

    /**
     * A dedicated TE converter whose main role is to remove encoded columns from `RowData` in some conditions
     * to avoid the column to be re-encoded later (e.g. by the categorical encoding) if it was not desired.
     */
    private static class TargetEncoderRowToRawDataConverter extends DefaultRowToRawDataConverter<TargetEncoderMojoModel> {
        
        private final TargetEncoderMojoModel _teModel;
        
        
        public TargetEncoderRowToRawDataConverter(TargetEncoderMojoModel teModel,
                                                  Map<String, Integer> columnToOffsetIdx,
                                                  Map<Integer, CategoricalEncoder> offsetToEncoder,
                                                  EasyPredictModelWrapper.ErrorConsumer errorConsumer,
                                                  EasyPredictModelWrapper.Config config) {
            super(columnToOffsetIdx,
                  offsetToEncoder,
                  errorConsumer, 
                  config);
            _teModel = teModel;
        }
    
        @Override
        public double[] convert(RowData data, double[] rawData) throws PredictException {
            addInteractions(data);
            double[] converted = super.convert(data, rawData);
            for (ColumnsToSingleMapping colMap : _teModel._inencMapping) { // remove interaction columns
                if (colMap.from().length > 1) data.remove(colMap.toSingle());
            }
            if (!_teModel._keepOriginalCategoricalColumns) {
                for (String teColumn : _teModel._encodingsByCol.keySet()) data.remove(teColumn);
            }
            return converted;
        }
        
        private void addInteractions(RowData data) {
            for (ColumnsToSingleMapping colMap : _teModel._inencMapping) {
                String[] colGroup = colMap.from();
                if (colGroup.length == 1) continue;
                
                String interaction = _teModel.computeCategorical(colMap, data);
                data.put(colMap.toSingle(), interaction);
            }
        }
    }

    /**
     *  This virtual model is used to "trick" further transformers and especially CategoricalEncoding
     *  to provide it with a model/frame description that looks as if TE was already applied.
     */
    private static class VirtualTargetEncodedModel extends GenModel {
        
        GenModel _m;
        
        public VirtualTargetEncodedModel(GenModel m, String[] names, String[][] domains, String responseColumn) {
            super(names, domains, responseColumn);
            _m = m;
        }
    
        @Override
        public ModelCategory getModelCategory() {
            return _m.getModelCategory();
        }
    
        @Override
        public String getUUID() {
            return _m.getUUID();
        }
    
        @Override
        public double[] score0(double[] row, double[] preds) {
            throw new IllegalStateException("This virtual model should not be called for scoring");
        }
    
        @Override
        public int getOrigNumCols() {
            return getNumCols();
        }
    
        @Override
        public String[] getOrigNames() {
            return getNames();
        }
    
        @Override
        public String[][] getOrigDomainValues() {
            return getDomainValues();
        }
    
        @Override
        public double[] getOrigProjectionArray() {
            return _m.getOrigProjectionArray();
        }
    }
}

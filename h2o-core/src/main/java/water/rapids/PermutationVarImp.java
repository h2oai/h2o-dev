package water.rapids;

import hex.*;
import water.fvec.Frame;
import water.fvec.Vec;
import water.util.TwoDimTable;
import water.util.VecUtils;

import java.util.*;

/**
 * Permutation Variable (feature) importance measures the increase in the prediction error of the model after permuting 
 * the variables's values, which breaks the relationship between the variables and the true outcome.
 * https://christophm.github.io/interpretable-ml-book/feature-importance.html
 *
 * Calculate permutation variables importance, by shuffling randomly each variables of the training Frame,
 * scoring the model with the newly created frame using One At a Time approach
 * and Morris method; creating TwoDimTable with relative, scaled, and percentage value
 *                             TwoDimTable with mean of the absolute value, and standard deviation of all features importance
 */

public class PermutationVarImp {

    public double[] _pVarImp; // permutation variables importance, (relative)
    
    private String _responseCol; 
    
    private String[] _var; 
    private String[] _varsToShuffle;
    public String[] _metrics;

    /**
     * Stores the metric to be used (loss function) original values and j-th variables's score metric values  
     */
    public class LocalMetric{ // do it as a string to get the metric from the user

        LocalMetric(String metric)  { mMetric = metric; }
        LocalMetric()               { mMetric = "mse"; } 
        String mMetric;
        double mOgMetric;
        double mVariablesMetric;
    }

    public LocalMetric _varImpMetric;
    public Map<String, Double> _varImpMap;
    TwoDimTable _permutationVarImp;
    private Model _model;
    private Frame _trainFr;

    /**
     * Constructor that stores the model, frame, response column, variable Strings and 
     * sets the allowed metrics
     * @param model trained model
     * @param fr traiing frame
     */
    public PermutationVarImp(Model model, Frame fr) {
        _model = model;
        _trainFr = fr;
        _responseCol = _model._parms._response_column;
        _var = _trainFr.names();
        _metrics = new String[]{"r2", "mse", "rmse", "gini coefficient", "f1", "logloss", "auc"};
    }
    
    /**
     * Creates a new array of Strings without the response column and ignored columns
     */
    public void removeResCol(){
        List<String> list = new ArrayList<>(Arrays.asList(_trainFr.names()));
        // remove ignored columns & response column
        if (_model._parms._ignored_columns != null)
            for (String s : _model._parms._ignored_columns) list.remove(s);
        list.remove(_responseCol);
        _varsToShuffle = list.toArray(new String[0]);
        
        // alloc permutation variable importance array 
        _pVarImp = new double[_varsToShuffle.length];
    }

    
    /**
     * Returns the metric (loss function) selected by the user (mse is default)
     * @throws MetricNotFoundException if metric could not be loaded 
     */
    private double getMetric(ModelMetrics mm) throws MetricNotFoundException {
        double metric = Double.NaN;
        assert mm != null;
        try{
            switch (_varImpMetric.mMetric){
                case "r2":  metric = _model.r2();
                    break;
                case "mse": metric = mm.mse();
                    break;
                case "rmse": metric = mm.rmse();
                    break;
                case "gini coefficient": metric = mm.auc_obj()._gini;
                    break;
                case  "logloss": metric = _model.logloss();
                    ModelCategory mc = _model._output.getModelCategory();
                    if (mc == ModelCategory.Binomial)
                        metric = ((ModelMetricsBinomial)mm).logloss();
                    else if (mc == ModelCategory.Multinomial)
                        metric = ((ModelMetricsMultinomial)mm).logloss();
                    else throw new MetricNotFoundException( _model._output.getModelCategory().name() + " with " + _varImpMetric.mMetric + " not found ");
                    break; 
                case "auc": metric = mm.auc_obj()._auc;
                    break;
                default:
                    throw new MetricNotFoundException("Metric not supported " + _varImpMetric.mMetric);
            }
        } catch (MetricNotFoundException |NullPointerException e){ 
            System.err.println("ModelMetricCalculation  " + _model._key);
            e.printStackTrace();
        }
        if(Double.isNaN(metric))
            throw new MetricNotFoundException("Model doesn't support the metric following metric " + _varImpMetric.mMetric);
        return metric;
    }
    
    /**
     * Set the metric upon training the model (original ~ Og)
     */
    public void setOgMetric() {
        try{
            _varImpMetric.mOgMetric = getMetric(ModelMetrics.getFromDKV(_model, _model._parms.train()));
        } catch (MetricNotFoundException e){
            System.err.println("Metric " + _varImpMetric.mMetric + " not supported for :" + _model._key);
            e.printStackTrace();
        }
    }
    
    /**
     * Set the metric of the feature that is permuted
     */
    private void setVariablesMetric(int var){
        try{
            // divide original metric with metric value obtained from shuffled variable 
            _varImpMetric.mVariablesMetric = getMetric(ModelMetrics.getFromDKV(_model, _trainFr)) - _varImpMetric.mOgMetric;
        } catch (MetricNotFoundException e){
            System.err.println("Metric " + _varImpMetric.mMetric + " not supported for :" + _model._key);
            e.printStackTrace();
        }
        _pVarImp[var] = _varImpMetric.mVariablesMetric;
    }

    /**
     *  If the user specifies a metric store it to the LocalMetric class*
     * @return TwoDimTable of Permutation Feature Importance scores
     */
    public TwoDimTable getPermutationVarImp(String metric)  {
        try {
            if (!Arrays.asList(_metrics).contains(metric.toLowerCase()))
                throw new MetricNotFoundException("Permutation Variable Importance doesnt support " + metric + " for model " + _model._key );
            } catch (MetricNotFoundException e) {
            System.err.println("Metric " + _varImpMetric.mMetric + " not supported for :" + _model._key);
            e.printStackTrace();
        }

        _varImpMetric = new LocalMetric(metric.toLowerCase());
        return PermutationVarImportance();
    }

    /**
     * No metric was selected by the user so MSE will be used 
     * @return TwoDimTable of Permutation Feature Importance scores
     */
    public TwoDimTable getPermutationVarImp() {
        // put all the metrics in a class for structure
        _varImpMetric = new LocalMetric();
        assert _varImpMetric.mMetric.equals("mse");  
        return PermutationVarImportance();
    }


    /**
     * Check If the variable is in ignored parameters on the model
     * @param var Vec to be shuffled
     * @return
     */
    public boolean isIgnored(String var) {
        if (_model._parms._ignored_columns == null) 
                return false;
        return Arrays.asList(_model._parms._ignored_columns).contains(var);
    }
    
    /**
     * permute the feature's values breaking the relationship between the feature and the true outcome.
     * Then we score the model again and calculate the loss function, and creating a TwoDimTable.
     */
    public TwoDimTable PermutationVarImportance(){
        removeResCol(); 
        setOgMetric(); // get the metric value from the model
        _varImpMap = new HashMap<>(_varsToShuffle.length);

        int id = 0;
        for (int f = 0; f < _trainFr.numCols(); f++)
        {
            // skip for response column
            if (_var[f].equals(_responseCol) || isIgnored(_var[f]))
                continue;

            //shuffle values of feature
            Vec shuffled_feature = VecUtils.ShuffleVec(_trainFr.vec(_var[f]), _trainFr.vec(_var[f]).makeCopy());
            Vec og_feature = _trainFr.replace(f, shuffled_feature);

            // score the model again and compute diff
            Frame new_score = _model.score(_trainFr);

            // set and add new metrics ~ fills @param _p_var_imp needed for ModelMetrics.calcVarImp()
            setVariablesMetric(id);
            
            //return the original data
            _trainFr.replace(f, og_feature);

            // Create Map
            _varImpMap.put(_var[f], _pVarImp[id++]);

            new_score.remove();
            shuffled_feature.remove();
        }
        // Create TwoDimTable having (Relative + Scaled + percentage) importance 
        _permutationVarImp = ModelMetrics.calcVarImp(_pVarImp, _varsToShuffle);
        return _permutationVarImp;
    }


    /**
     * Default is set to return the Relative value of the Permutation Feature Importance (PFI)
     */
    public TwoDimTable oat(){ return oat(0); } 
    
    /**
     * @param type {0,1,2}
     * type 0: Relative value of PFI
     * type 1: Scaled value of PFI
     * type 2: Percentage value of PFI
     */
    public TwoDimTable oat(int type) {
        int r = 4; // set 4 to 10
        
        // Using maps to not lose which Variable has Which score as to sometimes the ordering changes
        List<Map<String, Double>> listOfMaps = new ArrayList<Map<String, Double>>();
        Map<String, Double> meanOfInfluence = new HashMap<>();
        Map<String, Double> meanOfInfluenceAbsVal = new HashMap<>();
        
        // Generate r tables of Feature importance differently shuffled
        for (int i = 0; i < r; i++) {
            // Get permutationVarImp table
            TwoDimTable morrisFis = getPermutationVarImp();
            
            // On first iteration fill values
            if (meanOfInfluence.isEmpty()) {
                // _varImpMap "variable" -> Importance <String, Double> map
                meanOfInfluence.putAll(_varImpMap);
                // First iteration the maps are empty so just "copying" the values
                for (Map.Entry<String, Double> var : meanOfInfluence.entrySet()) {
                    meanOfInfluenceAbsVal.put(var.getKey(), Math.abs(var.getValue()));
                    meanOfInfluence.put(var.getKey(), Math.abs(var.getValue()));
                }
            }   else    {
                // The formula is: 1 / r * (Sum_{i=0}^r | PVI values |)  
                for (Map.Entry<String, Double> var : meanOfInfluence.entrySet()) {
                    // replace the value with the previous one + this iterations one
                    meanOfInfluence.replace(var.getKey(), var.getValue(), var.getValue() + _varImpMap.get(var.getKey()));
                    meanOfInfluenceAbsVal.replace(var.getKey(), var.getValue(), var.getValue() + Math.abs(_varImpMap.get(var.getKey())));
                }
            }
            // creating a list of VarImps to calculate standard deviation
            listOfMaps.add(_varImpMap);
        }
        
        // divide values of the Map by r
        for (Map.Entry<String, Double> var : meanOfInfluence.entrySet()) {
            meanOfInfluence.replace(var.getKey(), var.getValue(), var.getValue() / r);
        }
        for (Map.Entry<String, Double> var : meanOfInfluenceAbsVal.entrySet()) {
            meanOfInfluenceAbsVal.replace(var.getKey(), var.getValue(), var.getValue() / r);
        }

        // Calculate the meanOfInfluence of the absolute value of each feature's importance 
        Map<String, Double> standardDevFI = new HashMap<>();
        // Similrarly as before there's a sum hence the for loop for r
        for (int i = 0 ; i < r ; i++){
            // initialy just "copy" data
            if (standardDevFI.isEmpty()){
                for (Map.Entry<String, Double> var : listOfMaps.get(i).entrySet()) {
                    standardDevFI.put(var.getKey(), Math.pow(var.getValue() - meanOfInfluence.get(var.getKey()), 2));
                }
            } else {
                // Go through r calculations of PVI and apply the formula
                for (Map.Entry<String, Double> var : listOfMaps.get(i).entrySet()) {
                    standardDevFI.replace(var.getKey(), var.getValue(), var.getValue() + Math.pow(var.getValue() - meanOfInfluence.get(var.getKey()), 2));
                }
            }
        }
        
        // Divide every value by r
        for (Map.Entry<String, Double> var : standardDevFI.entrySet()) {
            standardDevFI.replace(var.getKey(), var.getValue(), Math.sqrt(var.getValue() / r));
        }

        // Contains the meanOfInfluence of the absolute value and standard deviation of each feature's importance, hence the [2]
        double [][] response = new double [meanOfInfluenceAbsVal.size()][2];
        
        // Create a matrix to fill the TwoDimTable
        int i = 0;
        for (String var : _varsToShuffle) {
            response[i][0] = meanOfInfluenceAbsVal.get(var); 
            response[i++][1] = standardDevFI.get(var);
        }
        
        // Necessary to create the TwoDimTable
        String [] colTypes = new String[2];
        String [] colFormats = new String[2];
        Arrays.fill(colTypes, "double");
        Arrays.fill(colFormats, "%5f");
        
        return new TwoDimTable("One At a Time", null, _varsToShuffle, new String [] {"Mean of the absolute value", "standard deviation"},
                    colTypes, colFormats, "Permutation Variable Importance", new String[_varsToShuffle.length][], response);
    }
}


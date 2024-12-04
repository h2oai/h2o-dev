package hex.knn;


import water.MRTask;
import water.fvec.Chunk;
import water.fvec.Vec;
import water.util.ArrayUtils;

public class KNNScoringTask extends MRTask<KNNScoringTask> {

    public int _k;
    public double[] _queryData;
    public KNNDistance _distance;
    public TopNTreeMap<KNNKey, Integer> _distancesMap;
    public int _idIndex;
    public int _responseIndex;
    public byte _idColumnType;
    public int _domainSize;

    /**
     *
     */
    public KNNScoringTask(double[] query, int k, int domainSize, KNNDistance distance, int idIndex, byte idType, int responseIndex){
        this._k = k;
        this._queryData = query;
        this._distance = distance;
        this._responseIndex = responseIndex;
        this._idIndex = idIndex;
        this._idColumnType = idType;
        this._distancesMap = new TopNTreeMap<>(_k);
        this._domainSize = domainSize;
    }

    @Override
    public void map(Chunk[] cs) {
        int inputColNum = cs.length-2;
        int inputRowNum = cs[0]._len;
        for (int j = 0; j < inputRowNum; j++) { // go over all input data rows
            String inputDataId = _idColumnType == Vec.T_STR ? cs[_idIndex].stringAt(j) : String.valueOf(cs[_idIndex].at8(j));
            int inputDataCategory = (int) cs[_responseIndex].at8(j);
            double[] distValues = _distance.initializeValues();
            for (int k = 0; k < inputColNum; k++) { // go over all columns
                double queryColData = _queryData[k];
                double inputColData = cs[k].atd(j);
                distValues = _distance.calculateValues(queryColData, inputColData, distValues);
            }
            double dist = _distance.result(distValues);
            _distancesMap.put(new KNNKey(inputDataId, dist), inputDataCategory);
        }
    }

    @Override
    public void reduce(KNNScoringTask mrt) {
        this._distancesMap.putAll(mrt._distancesMap);
    }
    
    public double[] score(){
        double[] scores = new double[_domainSize+1];
        assert _distancesMap.size() <= _k: "Distances map size should be <= _k";
        for (int value: _distancesMap.values()){
            scores[value+1]++;
        }
        for (int i = 1; i < _domainSize+1; i++) {
            if(scores[i] != 0) {
                scores[i] = scores[i]/_k;
            }
        }
        scores[0] = ArrayUtils.maxIndex(scores);
        return scores;
    }
}
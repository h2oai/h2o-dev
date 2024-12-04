package hex.knn;

import hex.*;
import org.junit.Assert;
import org.junit.BeforeClass;
import org.junit.Test;
import water.DKV;
import water.TestUtil;
import water.fvec.Frame;
import water.fvec.TestFrameBuilder;
import water.fvec.Vec;
import water.util.TwoDimTable;


public class KNNTest extends TestUtil {

    @BeforeClass() public static void setup() { stall_till_cloudsize(1); }

    @Test
    public void testIris() {
        KNNModel knn = null;
        Frame fr = null;
        Frame preds = null;
        Frame distances = null;
        try {
            fr = parseTestFile("smalldata/iris/iris_wheader.csv");
            
            String idColumn = "id";
            String response = "class";

            fr.add(idColumn, createIdVec(fr.numRows(), Vec.T_NUM));
            DKV.put(fr);
            KNNModel.KNNParameters parms = new KNNModel.KNNParameters();
            parms._train = fr._key;
            parms._k = 3;
            parms._distance = new EuclideanDistance();
            parms._response_column = response;
            parms._id_column = idColumn;
            parms._auc_type = MultinomialAucType.MACRO_OVR;

            parms._seed = 42;
            KNN job = new KNN(parms);
            knn = job.trainModel().get();
            Assert.assertNotNull(knn);
            
            distances = knn._output.getDistances();
            Assert.assertNotNull(distances);
            
            preds = knn.score(fr);
            Assert.assertNotNull(preds);

            ModelMetricsMultinomial mm = (ModelMetricsMultinomial) ModelMetrics.getFromDKV(knn, parms.train());
            ModelMetricsMultinomial mm1 = (ModelMetricsMultinomial) knn._output._training_metrics;
            Assert.assertEquals(mm.auc(), mm1.auc(), 0);
            
            // test after KNN API will be ready
            //knn.testJavaScoring(fr, preds, 0);
            
        } finally {
            if (knn != null){
                knn.delete();
            }
            if (distances != null){
                distances.delete();
            }
            if(fr != null) {
                fr.delete();
            }
            if(preds != null){
                preds.delete();
            }
        }
    }

    @Test
    public void testSimpleFrameEuclidean() {
        KNNModel knn = null;
        Frame fr = null;
        Frame preds = null;
        Frame distances = null;
        try {
            fr = generateSimpleFrame();

            String idColumn = "id";
            String response = "class";

            DKV.put(fr);
            KNNModel.KNNParameters parms = new KNNModel.KNNParameters();
            parms._train = fr._key;
            parms._k = 2;
            parms._distance = new EuclideanDistance();
            parms._response_column = response;
            parms._id_column = idColumn;
            parms._auc_type = MultinomialAucType.MACRO_OVR;

            parms._seed = 42;
            KNN job = new KNN(parms);
            knn = job.trainModel().get();
            Assert.assertNotNull(knn);

            distances = knn._output.getDistances();
            Assert.assertNotNull(distances);

            Assert.assertEquals(distances.vec(0).at8(0), 1);
            Assert.assertEquals(distances.vec(1).at(0), 0.0, 0);
            Assert.assertEquals(distances.vec(2).at(0), 1.414, 10e-3);
            Assert.assertEquals(distances.vec(3).at8(0), 1);
            Assert.assertEquals(distances.vec(4).at8(0), 2);
            Assert.assertEquals(distances.vec(5).at8(0), 1);
            Assert.assertEquals(distances.vec(6).at8(0),1);

            Assert.assertEquals(distances.vec(0).at8(1), 2);
            Assert.assertEquals(distances.vec(1).at(1), 0.0, 0);
            Assert.assertEquals(distances.vec(2).at(1), 1.414, 10e-3);
            Assert.assertEquals(distances.vec(3).at8(1), 2);
            Assert.assertEquals(distances.vec(4).at8(1), 1);
            Assert.assertEquals(distances.vec(5).at8(1), 1);
            Assert.assertEquals(distances.vec(6).at8(1), 1);

            preds = knn.score(fr);
            Assert.assertNotNull(preds);

            Assert.assertEquals(preds.vec(0).at8(0), 1);
            Assert.assertEquals(preds.vec(1).at(0), 0.0, 0);
            Assert.assertEquals(preds.vec(2).at(0), 1.0, 0);

            Assert.assertEquals(preds.vec(0).at8(3), 0);
            Assert.assertEquals(preds.vec(1).at(3), 0.5, 0);
            Assert.assertEquals(preds.vec(2).at(3), 0.5, 0);

            ModelMetricsBinomial mm = (ModelMetricsBinomial) ModelMetrics.getFromDKV(knn, parms.train());
            Assert.assertNotNull(mm);
            Assert.assertEquals(mm.auc(), 0.75, 0);
            
            
        } finally {
            if (knn != null){
                knn.delete();
            }
            if (distances != null){
                distances.delete();
            }
            if(fr != null) {
                fr.delete();
            }
            if(preds != null){
                preds.delete();
            }
        }
    }


    @Test
    public void testSimpleFrameManhattan() {
        KNNModel knn = null;
        Frame fr = null;
        Frame preds = null;
        Frame distances = null;
        try {
            fr = generateSimpleFrame();

            String idColumn = "id";
            String response = "class";

            DKV.put(fr);
            KNNModel.KNNParameters parms = new KNNModel.KNNParameters();
            parms._train = fr._key;
            parms._k = 2;
            parms._distance = new ManhattanDistance();
            parms._response_column = response;
            parms._id_column = idColumn;
            parms._auc_type = MultinomialAucType.MACRO_OVR;

            parms._seed = 42;
            KNN job = new KNN(parms);
            knn = job.trainModel().get();
            Assert.assertNotNull(knn);

            distances = knn._output.getDistances();
            Assert.assertNotNull(distances);

            Assert.assertEquals(distances.vec(0).at8(0), 1);
            Assert.assertEquals(distances.vec(1).at(0), 0.0, 0);
            Assert.assertEquals(distances.vec(2).at(0), 2.0, 0);
            Assert.assertEquals(distances.vec(3).at8(0), 1);
            Assert.assertEquals(distances.vec(4).at8(0), 2);
            Assert.assertEquals(distances.vec(5).at8(0), 1);
            Assert.assertEquals(distances.vec(6).at8(0),1);

            Assert.assertEquals(distances.vec(0).at8(1), 2);
            Assert.assertEquals(distances.vec(1).at(1), 0.0, 0);
            Assert.assertEquals(distances.vec(2).at(1), 2.0, 0);
            Assert.assertEquals(distances.vec(3).at8(1), 2);
            Assert.assertEquals(distances.vec(4).at8(1), 1);
            Assert.assertEquals(distances.vec(5).at8(1), 1);
            Assert.assertEquals(distances.vec(6).at8(1), 1);
            
            preds = knn.score(fr);
            Assert.assertNotNull(preds);
            
            Assert.assertEquals(preds.vec(0).at8(0), 1);
            Assert.assertEquals(preds.vec(1).at(0), 0.0, 0);
            Assert.assertEquals(preds.vec(2).at(0), 1.0, 0);

            Assert.assertEquals(preds.vec(0).at8(3), 0);
            Assert.assertEquals(preds.vec(1).at(3), 0.5, 0);
            Assert.assertEquals(preds.vec(2).at(3), 0.5, 0);
            
            ModelMetricsBinomial mm = (ModelMetricsBinomial) ModelMetrics.getFromDKV(knn, parms.train());
            Assert.assertNotNull(mm);
            Assert.assertEquals(mm.auc(), 0.75, 0);
            
        } finally {
            if (knn != null){
                knn.delete();
            }
            if (distances != null){
                distances.delete();
            }
            if(fr != null) {
                fr.delete();
            }
            if(preds != null){
                preds.delete();
            }
        }
    }

    private Frame generateSimpleFrame(){
        return new TestFrameBuilder()
                .withColNames("id", "C0", "C1", "class")
                .withVecTypes(Vec.T_NUM, Vec.T_NUM, Vec.T_NUM, Vec.T_CAT)
                .withDataForCol(0, ari(1, 2, 3, 4))
                .withDataForCol(1, ard(0.0, 1.0, 2.0, 3.0))
                .withDataForCol(2, ard(0.0, 1.0, 0.0, 1.0))
                .withDataForCol(3, ar("1", "1", "0", "0"))
                .build();
    }
}
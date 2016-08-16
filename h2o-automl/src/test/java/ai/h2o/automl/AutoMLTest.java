package ai.h2o.automl;


import org.junit.BeforeClass;
import org.junit.Test;
import water.Key;
import water.fvec.Frame;

public class AutoMLTest extends TestUtil {

  @BeforeClass public static void setup() { stall_till_cloudsize(1); }

//  @Test public void histSmallCats() {
//    Frame fr = null;
//    AutoML aml = null;
//    try {
//      fr = parse_test_file(Key.make("a.hex"), "smalldata/iris.csv");
//      aml = new AutoML(Key.<AutoML>make(),"iris_wheader", fr, 4, "", -1, -1, false, null, true);
//      aml.learn();
//    } finally {
//      if(fr!=null)  fr.delete();
//      if(aml!=null) aml.delete();
//    }
//  }
//
//  @Test public void checkMeta() {
//    Frame fr=null;
//    AutoML aml=null;
//    try {
//      fr = parse_test_file(Key.make("a.hex"), "smalldata/iris.csv");
//      aml = new AutoML(Key.<AutoML>make(),"iris_wheader",fr, 4, "", -1, -1, false, null, true);
//      aml.learn();
//
//      // sepal_len column
//      // check the third & fourth moment computations
//      Assert.assertTrue(aml._fm._cols[0]._thirdMoment == 0.17642222222222248);
//      Assert.assertTrue(aml._fm._cols[0]._fourthMoment == 1.1332434671886653);
//
//      // check skew and kurtosis
//      Assert.assertTrue(aml._fm._cols[0]._skew == 0.31071214388181395);
//      Assert.assertTrue(aml._fm._cols[0]._kurtosis == 2.410255837401182);
//    } finally {
//      // cleanup
//      if(fr!=null)  fr.delete();
//      if(aml!=null) aml.delete();
//    }
//  }

  @Test public void SanTanderTest() {
    Frame fr=null;
    AutoML aml=null;
    try {
      aml=AutoML.makeAutoML(Key.<AutoML>make(),"/Users/spencer/Downloads/train.csv.zip", null, "TARGET","MSE", 3600,-1,true,null,true);
      aml.learn();
    } finally {
      // cleanup
      if(aml!=null) aml.delete();
    }
  }
}

package hex.deeplearning;

import hex.Model;
import hex.deeplearning.DeepLearningModel.DeepLearningParameters;
import org.apache.commons.lang.math.LongRange;
import org.junit.BeforeClass;
import org.junit.Test;
import water.Key;
import water.TestUtil;
import water.fvec.Frame;
import water.rapids.Rapids;
import water.rapids.Val;
import water.rapids.vals.ValFrame;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

public class DeepLearningSHAPTest extends TestUtil {
  
  /*
   NOTE: These test do not test all required properties for SHAP. 
   To be more sure after doing some changes to the SHAP, please run the python test:
   h2o-py/tests/testdir_misc/pyunit_SHAP.py 
  */

  @BeforeClass
  public static void setup() {
    stall_till_cloudsize(1);
  }


  @Test
  public void testClassificationCompactSHAP() {
    Frame fr = parseTestFile("smalldata/titanic/titanic_expanded.csv");
    Frame bgFr = fr.deepSlice(new LongRange(0, 50).toArray(), null);
    Frame test = fr.deepSlice(new LongRange(51, 101).toArray(), null);
    DeepLearningModel model = null;
    Frame scored = null;
    Frame contribs = null;
    Frame res = null;
    try {
      // Launch Deep Learning
      DeepLearningParameters params = new DeepLearningParameters();
      params._train = fr._key;
      params._epochs = 5;
      params._response_column = "survived";

      model = new DeepLearning(params).trainModel().get();

      assert model != null;
      scored = model.score(test);
      contribs = model.scoreContributions(test, Key.make(), null,
              new Model.Contributions.ContributionsOptions().setOutputFormat(Model.Contributions.ContributionsOutputFormat.Compact),
              bgFr);

      assert fr.numCols() >= contribs.numCols();

      Val val = Rapids.exec("(sumaxis " + contribs._key + " 0 1)");
      assertTrue(val instanceof ValFrame);
      res = val.getFrame();
      assertColsEquals(scored, res, 2, 0, 1e-8);
    } finally {
      fr.delete();
      bgFr.delete();
      test.delete();
      if (null != res) res.delete();
      if (null != scored) scored.delete();
      if (null != contribs) contribs.delete();
      if (null != model) model.delete();
    }
  }


  @Test
  public void testClassificationOriginalSHAP() {
    Frame fr = parseTestFile("smalldata/titanic/titanic_expanded.csv");
    Frame bgFr = fr.deepSlice(new LongRange(0, 50).toArray(), null);
    Frame test = fr.deepSlice(new LongRange(51, 101).toArray(), null);
    DeepLearningModel model = null;
    Frame scored = null;
    Frame contribs = null;
    Frame res = null;
    try {
      // Launch Deep Learning
      DeepLearningParameters params = new DeepLearningParameters();
      params._train = fr._key;
      params._epochs = 5;
      params._response_column = "survived";

      model = new DeepLearning(params).trainModel().get();

      assert model != null;
      scored = model.score(test);
      contribs = model.scoreContributions(test, Key.make(), null,
              new Model.Contributions.ContributionsOptions().setOutputFormat(Model.Contributions.ContributionsOutputFormat.Original),
              bgFr);

      assert fr.numCols() < contribs.numCols();  // Titanic has categorical vars

      Val val = Rapids.exec("(sumaxis " + contribs._key + " 0 1)");
      assertTrue(val instanceof ValFrame);
      res = val.getFrame();
      assertColsEquals(scored, res, 2, 0, 1e-8);
    } finally {
      fr.delete();
      bgFr.delete();
      test.delete();
      if (null != res) res.delete();
      if (null != scored) scored.delete();
      if (null != contribs) contribs.delete();
      if (null != model) model.delete();
    }
  }


  @Test
  public void testRegressionCompactSHAP() {
    Frame fr = parseTestFile("smalldata/titanic/titanic_expanded.csv");
    Frame bgFr = fr.deepSlice(new LongRange(0, 50).toArray(), null);
    Frame test = fr.deepSlice(new LongRange(51, 101).toArray(), null);
    DeepLearningModel model = null;
    Frame scored = null;
    Frame contribs = null;
    Frame res = null;
    try {
      // Launch Deep Learning
      DeepLearningParameters params = new DeepLearningParameters();
      params._train = fr._key;
      params._epochs = 5;
      params._response_column = "fare";

      model = new DeepLearning(params).trainModel().get();

      assert model != null;
      scored = model.score(test);
      contribs = model.scoreContributions(test, Key.make(), null,
              new Model.Contributions.ContributionsOptions().setOutputFormat(Model.Contributions.ContributionsOutputFormat.Compact),
              bgFr);

      assert fr.numCols() >= contribs.numCols();

      Val val = Rapids.exec("(sumaxis " + contribs._key + " 0 1)");
      assertTrue(val instanceof ValFrame);
      res = val.getFrame();
      assertColsEquals(scored, res, 0, 0, 1e-5);
    } finally {
      fr.delete();
      bgFr.delete();
      test.delete();
      if (null != res) res.delete();
      if (null != scored) scored.delete();
      if (null != contribs) contribs.delete();
      if (null != model) model.delete();
    }
  }


  @Test
  public void testRegressionOriginalSHAP() {
    Frame fr = parseTestFile("smalldata/titanic/titanic_expanded.csv");
    Frame bgFr = fr.deepSlice(new LongRange(0, 50).toArray(), null);
    Frame test = fr.deepSlice(new LongRange(51, 101).toArray(), null);
    DeepLearningModel model = null;
    Frame scored = null;
    Frame contribs = null;
    Frame res = null;
    try {
      // Launch Deep Learning
      DeepLearningParameters params = new DeepLearningParameters();
      params._train = fr._key;
      params._epochs = 5;
      params._response_column = "fare";

      model = new DeepLearning(params).trainModel().get();

      assert model != null;
      scored = model.score(test);
      contribs = model.scoreContributions(test, Key.make(), null,
              new Model.Contributions.ContributionsOptions().setOutputFormat(Model.Contributions.ContributionsOutputFormat.Original),
              bgFr);

      assert fr.numCols() < contribs.numCols(); // Titanic has categorical vars

      Val val = Rapids.exec("(sumaxis " + contribs._key + " 0 1)");
      assertTrue(val instanceof ValFrame);
      res = val.getFrame();
      assertColsEquals(scored, res, 0, 0, 1e-5);
    } finally {
      fr.delete();
      bgFr.delete();
      test.delete();
      if (null != res) res.delete();
      if (null != scored) scored.delete();
      if (null != contribs) contribs.delete();
      if (null != model) model.delete();
    }
  }

  private static void assertColsEquals(Frame expected, Frame actual, int colExpected, int colActual, double eps) {
    assertEquals(expected.numRows(), actual.numRows());
    for (int i = 0; i < expected.numRows(); i++) {
      assertEquals("Wrong sum in row " + i, expected.vec(colExpected).at(i), actual.vec(colActual).at(i), eps);
    }
  }
}

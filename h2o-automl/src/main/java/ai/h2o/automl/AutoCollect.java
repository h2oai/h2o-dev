package ai.h2o.automl;

import hex.Model;
import hex.ModelBuilder;
import hex.deeplearning.DeepLearning;
import hex.deeplearning.DeepLearningModel;
import hex.glm.GLM;
import hex.glm.GLMModel;
import hex.tree.drf.DRF;
import hex.tree.drf.DRFModel;
import hex.tree.gbm.GBM;
import hex.tree.gbm.GBMModel;
import water.H2O;
import water.fvec.Frame;

import java.sql.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Random;

import static water.util.RandomUtils.getRNG;


/**
 * AutoCollect collects frame metadata and score histories over a grid search on
 * the available h2o supervised learning methods. It stores all of this information
 * in a SQL db (hard-coded).
 *
 * Future enhancements will allow the user to specify where to store information.
 */
public class AutoCollect {

  public static int RFMAXDEPTH=50;
  public static int RFMAXNBINS=4096;
  public static int RFMAXNBINSCATS=4096;
  public static int RFMAXNTREES=1000;
  public static int RFMAXNROWS=50;

  private final static String[] DLGRIDDABLES = new String[]{
          "activation", "layers", "neurons", "epochs", "rho", "rate", "rate_annealing",
          "rate_decay", "momentum_ramp", "momentum_stable", "input_dropout_ratio", "l1",
          "l2", "max_w2", "initial_weight_distribution", "initial_weight_scale"
  };

  private HashSet<String> configs;  // set of configs across all runs

  public static final byte RF=0;
  public static final byte GBM=1;
  public static final byte GLM=2;
  public static final byte DL=3;
  public static final byte ANY=4; // randomly select algo on each iteration in collect

  private final int _seconds;  // time allocated per dataset
  private final String _path;  // directory of datasets to collect on
  private byte   _algo;        // algo to run collection on
  private static Connection conn=null;
  static {
    try {
      Class.forName("com.mysql.jdbc.Driver").newInstance();
    } catch (Exception ex) {
      System.out.println(ex.getMessage());
      throw new RuntimeException(ex);
    }

    try {
      conn = DriverManager.getConnection("jdbc:mysql://172.16.2.171/autocollect?user=spencer&password=spencer");
    } catch (SQLException ex) {
      System.out.println("SQLException: " + ex.getMessage());
      System.out.println("SQLState: " + ex.getSQLState());
      System.out.println("VendorError: " + ex.getErrorCode());
    }
  }

  public AutoCollect(int seconds, String path) {
    _seconds=seconds;
    _path=path;
    _algo=ANY;
    grabConfigs();
  }

  public AutoCollect(int seconds, String path, byte algo) {
    this(seconds, path);
    _algo=algo;
  }

  public void collect() {
    long start = System.currentTimeMillis();
    long elapsed = 0;
    while( elapsed <= _seconds ) {
      ModelBuilder builder = selectNewBuilder();
      Model m = (Model)builder.trainModel().get();
      elapsed = System.currentTimeMillis()-start;
    }
  }

  private void grabConfigs() {
    configs = new HashSet<>();
    for (String table : new String[]{"RFConfig", "GBMConfig", "DLConfig", "GLMConfig"}) {
      ResultSet rs = AutoCollect.query("SELECT ConfigID FROM " + table + ";");
      try {
        while (rs.next())
          configs.add(rs.getString(1));
      } catch (SQLException e) {
        e.printStackTrace();
      }
    }
  }

  private ModelBuilder selectNewBuilder() {
    byte algo=_algo;
    if( algo == ANY ) algo = (byte)getRNG(new Random().nextLong()).nextInt((int)ANY);
    switch(algo) {
      case RF:  return makeDRF();
      case GBM: return makeGBM();
      case GLM: return makeGLM();
      case DL:  return makeDL();
      default:
        throw new RuntimeException("Unknown algo type: " + algo);
    }
  }

  DRF makeDRF() { return new DRF(genRFParams());  }
  GBM makeGBM() { return new GBM(genGBMParams()); }
  GLM makeGLM() { return new GLM(genGLMParams()); }
  DeepLearning makeDL() { return new DeepLearning(genDLParams()); }

  private String getConfig(Model.Parameters parms) {
    String configID;
    if( parms instanceof DRFModel.DRFParameters) {
      DRFModel.DRFParameters p = (DRFModel.DRFParameters)parms;
      configID = "rf_"+_idFrame+"_"+p._mtries+"_"+p._sample_rate+"_"+p._ntrees+"_"+p._max_depth+"_"+p._min_rows+"_"+p._nbins+"_"+p._nbins_cats;
    } else if( parms instanceof GBMModel.GBMParameters ) {
      GBMModel.GBMParameters p = (GBMModel.GBMParameters)parms;
      configID = "gbm_"+_idFrame+"_"+p._ntrees+"_"+p._max_depth+"_"+p._min_rows+"_"+p._learn_rate+"_"+p._sample_rate+"_"+p._col_sample_rate+"_"+p._col_sample_rate_per_tree+"_"+p._nbins+"_"+p._nbins_cats;
    } else if( parms instanceof GLMModel.GLMParameters ) {
      GLMModel.GLMParameters p = (GLMModel.GLMParameters)parms;
      configID = "glm_"+_idFrame+"_"+p._alpha[0]+"_"+p._lambda[0];
    } else if( parms instanceof DeepLearningModel.DeepLearningParameters ) {
      DeepLearningModel.DeepLearningParameters p = (DeepLearningModel.DeepLearningParameters)parms;
      throw H2O.unimpl();
    } else
      throw new IllegalArgumentException("Don't know what to do with parameters: " + parms.getClass());
    return configID;
  }

  DRFModel.DRFParameters genRFParams() {
    String configID;
    DRFModel.DRFParameters p = new DRFModel.DRFParameters();
    HashMap<String, Object> config = new HashMap<>();
    config.put("idFrame", _idFrame);
    do {
      config.put("mtries", p._mtries = getRNG(new Random().nextLong()).nextInt(_preds.length));
      config.put("sample_rate", p._sample_rate = getRNG(new Random().nextLong()).nextFloat());
      config.put("ntrees", p._ntrees = getRNG(new Random().nextLong()).nextInt(RFMAXNTREES));
      config.put("max_depth", p._max_depth = getRNG(new Random().nextLong()).nextInt(RFMAXDEPTH));
      config.put("min_rows", p._min_rows = getRNG(new Random().nextLong()).nextInt(RFMAXNROWS));
      config.put("nbins", p._nbins = getRNG(new Random().nextLong()).nextInt(RFMAXNBINS));
      config.put("nbins_cats", p._nbins_cats = getRNG(new Random().nextLong()).nextInt(RFMAXNBINSCATS));
      config.put("ConfigID", configID = getConfig(p));
    } while(!isValidConfig(configID));
    configs.add(configID);
    pushMeta(config, config.keySet().toArray(new String[config.size()]), "RFConfig");
    return p;
  }

  GBMModel.GBMParameters genGBMParams() {
    String configID;
    GBMModel.GBMParameters p = new GBMModel.GBMParameters();
    HashMap<String, Object> config = new HashMap<>();
    config.put("idFrame", _idFrame);
    do {
      config.put("ntrees", p._ntrees = getRNG(new Random().nextLong()).nextInt(RFMAXNTREES));
      config.put("max_depth", p._max_depth = getRNG(new Random().nextLong()).nextInt(RFMAXDEPTH));
      config.put("min_rows", p._min_rows = getRNG(new Random().nextLong()).nextInt(RFMAXNROWS));
      config.put("learn_rate", p._learn_rate = getRNG(new Random().nextLong()).nextFloat());
      config.put("sample_rate", p._sample_rate = getRNG(new Random().nextLong()).nextFloat());
      config.put("col_sample_rate", p._col_sample_rate = getRNG(new Random().nextLong()).nextFloat());
      config.put("col_sample_rate_per_tree", p._col_sample_rate_per_tree = getRNG(new Random().nextLong()).nextFloat());
      config.put("nbins", p._nbins = getRNG(new Random().nextLong()).nextInt(RFMAXNBINS));
      config.put("nbins_cats", p._nbins_cats = getRNG(new Random().nextLong()).nextInt(RFMAXNBINSCATS));
      config.put("ConfigID", configID = getConfig(p));
    } while(!isValidConfig(configID));
    configs.add(configID);
    pushMeta(config, config.keySet().toArray(new String[config.size()]), "GBMConfig");
    return p;
  }

  GLMModel.GLMParameters genGLMParams() {
    String configID;
    GLMModel.GLMParameters p = new GLMModel.GLMParameters();
    HashMap<String, Object> config = new HashMap<>();
    config.put("idFrame", _idFrame);
    do {
      config.put("alpha", p._alpha = new double[]{getRNG(new Random().nextLong()).nextDouble()});
      // for lambda, place probability distribution heavily weighted to the left: [0,1e-3) U [1e-3, 1) U [1, 10)  ... with probs (0.8, 0.1, 0.1)
      double r = getRNG(new Random().nextLong()).nextDouble();
      double lambda=getRNG(new Random().nextLong()).nextDouble();
      if( r < 0.8 )
        while( lambda< 1e-3)
          lambda = getRNG(new Random().nextLong()).nextDouble();
      else if( 0.8 <= r && r < 0.9 )
        while (1e-3 <= lambda && lambda < 1 )
          lambda = getRNG(new Random().nextLong()).nextDouble();
      else
        while(lambda < 1 || lambda > 10)
          lambda = 1 + getRNG(new Random().nextLong()).nextDouble()*10;
        config.put("lambda", p._lambda = new double[]{lambda});
      config.put("ConfigId", configID = getConfig(p));
    } while(!isValidConfig(configID));
    configs.add(configID);
    pushMeta(config, config.keySet().toArray(new String[config.size()]), "GLMConfig");
    return p;
  }

  DeepLearningModel.DeepLearningParameters genDLParams() { throw H2O.unimpl(); }
    //          "activation", "layers", "neurons", "epochs", "rho", "rate", "rate_annealing",
//    "rate_decay", "momentum_ramp", "momentum_stable", "input_dropout_ratio", "l1",
//            "l2", "max_w2", "initial_weight_distribution", "initial_weight_scale"
//    String configID;
//    DeepLearningModel.DeepLearningParameters p = new DeepLearningModel.DeepLearningParameters();
//    do {
//      p._activation = DeepLearningModel.DeepLearningParameters.Activation.values()[getRNG(new Random().nextLong()).nextInt(DeepLearningModel.DeepLearningParameters.Activation.values().length)];
//      p._hidden
//      configID = getConfig(p);
//    } while(!isValidConfig(configID));
//    configs.add(configID);
//    return p;
//  }

  private boolean isValidConfig(String configID) { return !configs.contains(configID); }

  // member fields updated upon each call to computeMetaData
  private Frame _fr;
  private int[] _preds;
  private int[] _ignored;
  private int _resp;
  private boolean _isClass;
  private int _idFrame;
  public int computeMetaData(String datasetName, Frame f, int[] x, int y, boolean isClassification) {
    _fr=f; _preds=x; _resp=y; _isClass=isClassification; ignored(x, f);
    if( hasMeta(datasetName) ) return getidFrameMeta(datasetName);
    FrameMeta fm = new FrameMeta(f, y, x, datasetName, isClassification);
    HashMap<String, Object> frameMeta = FrameMeta.makeEmptyFrameMeta();
    fm.fillSimpleMeta(frameMeta);
    fm.fillDummies(frameMeta);
    _idFrame = pushFrameMeta(frameMeta);
    computeAndPushColMeta(fm, _idFrame);
    return _idFrame;
  }

  private void ignored(int[] x, Frame f) {
    ArrayList<Integer> ignored = new ArrayList<>();
    int xi=0;
    for(int i=0;i<f.numCols();++i) {
      if( xi < x.length && x[xi]==i ) xi++;
      else        ignored.add(i);
    }
    _ignored = new int[ignored.size()];
    for(int i=0;i<_ignored.length;++i)
      _ignored[i] = ignored.get(i);
  }

  private void computeAndPushColMeta(FrameMeta fm, int idFrameMeta) {
    fm.computeFrameMetaPass1();
    fm.computeVIFs();
    for(int i=0; i<fm._cols.length; ++i) {
      HashMap<String, Object> colMeta = ColMeta.makeEmptyColMeta();
      fm._cols[i].fillColMeta(colMeta, idFrameMeta);
      pushColMeta(colMeta);
    }
  }

  int getidFrameMeta(String datasetName) {
    String query = "SELECT idFrameMeta  AS id FROM FrameMeta WHERE DataSetName=\"" + datasetName + "\";";
    ResultSet rs = query(query);
    try {
      rs.next();
      return rs.getInt(1);
    } catch( SQLException ex) {
      System.out.println("SQLException: " + ex.getMessage());
      System.out.println("SQLState: " + ex.getSQLState());
      System.out.println("VendorError: " + ex.getErrorCode());
      throw new RuntimeException("Failed to retrieve ID for frame: " + datasetName);
    }
  }

  boolean hasMeta(String datasetName) {
    String query = "SELECT COUNT(*) AS cnt FROM FrameMeta WHERE DataSetName=\"" + datasetName + "\";";
    ResultSet rs = query(query);
    try {
      rs.next();
      if (rs.getInt(1) == 1) return true;
    } catch( SQLException ex) {
      System.out.println("SQLException: " + ex.getMessage());
      System.out.println("SQLState: " + ex.getSQLState());
      System.out.println("VendorError: " + ex.getErrorCode());
    }
    return false;
  }

  // up to the caller to close the ResultSet
  // TODO: use AutoCloseable
  public static ResultSet query(String query) {
    Statement s;
    ResultSet rs;
    try {
      s = conn.createStatement();
      rs = s.executeQuery(query);
      return rs;
    } catch (SQLException ex) {
      System.out.println("SQLException: " + ex.getMessage());
      System.out.println("SQLState: " + ex.getSQLState());
      System.out.println("VendorError: " + ex.getErrorCode());
    }
    throw new RuntimeException("Query failed");
  }

  public static int update(String query) {
    Statement s;
    try {
      s = conn.createStatement();
      s.executeUpdate(query, Statement.RETURN_GENERATED_KEYS);
      ResultSet genKeys = s.getGeneratedKeys();
      genKeys.next();
      return genKeys.getInt(1); // return the last insertID
    } catch (SQLException ex) {
      System.out.println("STATEMENT: " + query);
      System.out.println("SQLException: " + ex.getMessage());
      System.out.println("SQLState: " + ex.getSQLState());
      System.out.println("VendorError: " + ex.getErrorCode());
    }
    throw new RuntimeException("Query failed");
  }

  private int pushFrameMeta(HashMap<String,Object> fm) { return pushMeta(fm, FrameMeta.METAVALUES, "FrameMeta"); }
  private int pushColMeta  (HashMap<String,Object> cm) { return pushMeta(cm, ColMeta.METAVALUES, "ColMeta"); }
  private int pushMeta(HashMap<String, Object> fm, String[] metaValues, String tableName) {
    StringBuilder sb = new StringBuilder("INSERT INTO " + tableName + " (");
    sb.append(collapseStringArray(metaValues)).append(") \n");
    sb.append("VALUES (");
    int i=0;
    for(String k: metaValues) {
      sb.append("'").append(fm.get(k)).append("'");
      if(i++==fm.size()-1) sb.append(");");
      else sb.append(",");
    }
    return update(sb.toString());
  }

  static String collapseStringArray(String[] strs) {
    StringBuilder sb = new StringBuilder();
    for(int i=0;i<strs.length;++i) {
      sb.append(strs[i]);
      if( i==strs.length-1 ) return sb.toString();
      sb.append(",");
    }
    throw new RuntimeException("Should never be here");
  }
}

package hex.genmodel.attributes;

import com.google.gson.JsonObject;
import hex.ModelCategory;
import hex.genmodel.MojoModel;
import hex.genmodel.algos.tree.SharedTreeMojoModel;
import hex.genmodel.attributes.metrics.MojoModelMetrics;
import hex.genmodel.attributes.metrics.MojoModelMetricsBinomial;
import hex.genmodel.attributes.metrics.MojoModelMetricsMultinomial;
import hex.genmodel.attributes.metrics.MojoModelMetricsRegression;

import java.util.Arrays;

public class SharedTreeModelAttributes extends ModelAttributes {

  private final VariableImportances _variableImportances;
  private final MojoModelMetrics _trainingMetrics;

  public <M extends SharedTreeMojoModel> SharedTreeModelAttributes(JsonObject modelJson, M model) {
    super(modelJson);
    _variableImportances = extractVariableImportances(modelJson, model);
    final MojoModelMetrics mojoModelMetrics = determineModelMetricsType(model._category);

    ModelJsonReader.fillObject(mojoModelMetrics, modelJson, "output.training_metrics");
    _trainingMetrics = mojoModelMetrics;
  }

  private static MojoModelMetrics determineModelMetricsType(final ModelCategory modelCategory) {
    switch (modelCategory) {
      case Unknown:
        return new MojoModelMetrics();
      case Binomial:
        return new MojoModelMetricsBinomial();
      case Multinomial:
        return new MojoModelMetricsMultinomial();
      case Regression:
        return new MojoModelMetricsRegression();
      case Ordinal:
      case Clustering:
      case AutoEncoder:
      case DimReduction:
      case WordEmbedding:
      case CoxPH:
      case AnomalyDetection:
      default:
        return new MojoModelMetrics(); // Basic model metrics if nothing else is available
    }
  }

  private VariableImportances extractVariableImportances(final JsonObject modelJson, final MojoModel model) {
    final Table table = ModelJsonReader.readTable(modelJson, "output.variable_importances");
    if (table == null) return null;
    final double[] relativeVarimps = new double[table.rows()];
    final String[] varNames = new String[table.rows()];
    final int varImportanceCol = table.findColumnIndex("Relative Importance");
    final int varNameCol = table.findColumnIndex("Variable");
    if (varImportanceCol == -1) return null;
    if (varNameCol == -1) return null;
    for (int i = 0; i < table.rows(); i++) {
      relativeVarimps[i] = (double) table.getCell(varImportanceCol, i);
      varNames[i] = (String) table.getCell(varNameCol, i);
    }

    return new VariableImportances(varNames, relativeVarimps);
  }

  /**
   * @return A {@link VariableImportances} instance with variable importances for each feature used.
   */
  public VariableImportances getVariableImportances() {
    return _variableImportances;
  }
  
  public MojoModelMetrics getTrainingMetrics(){
    return _trainingMetrics;
  }
}

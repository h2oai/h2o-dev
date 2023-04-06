package hex.genmodel.mojopipeline.transformers;

import ai.h2o.mojos.runtime.api.backend.ReaderBackend;
import ai.h2o.mojos.runtime.frame.MojoFrame;
import ai.h2o.mojos.runtime.frame.MojoFrameMeta;
import ai.h2o.mojos.runtime.transforms.MojoTransform;
import ai.h2o.mojos.runtime.transforms.MojoTransformBuilderFactory;

import java.util.HashMap;
import java.util.Map;

public class ToNumericConversion extends MojoTransform {

    ToNumericConversionFunction _function;

    ToNumericConversion(int[] iindices, int[] oindices, ToNumericConversionFunction function) {
        super(iindices, oindices);
        _function = function;
    }

    @Override
    public void transform(MojoFrame frame) {
        Object input = frame.getColumnData(iindices[0]);
        double[] o = (double[]) frame.getColumnData(oindices[0]);
        if (input instanceof double[]){
            double[] a = (double[]) input;
            for (int i = 0, nrows = frame.getNrows(); i < nrows; i++) {
                o[i] = a[i];
            }
        } else {
            String[] a = (String[]) input;
            for (int i = 0, nrows = frame.getNrows(); i < nrows; i++) {
                if (a[i] == null) {
                    o[i] = Double.NaN;
                } else {
                    o[i] = _function.call(a[i]);
                }
            }
        }
    }

   interface ToNumericConversionFunction {
        void initialize(Map<String, Object> params);
        double call(String value);
    }

    public static class Factory implements MojoTransformBuilderFactory {
        
        private static final HashMap<String,ToNumericConversionFunction> _supportedFunctions = 
            new HashMap<String,ToNumericConversionFunction>() {{
                put("as.numeric", new ToNumericConversionFunction() {
                    @Override
                    public void initialize(Map<String, Object> params) {}

                    @Override
                    public double call(String value) { return Double.parseDouble(value); }
                });
                put("as.Date", new ToNumericConversionFunction() {
                    @Override
                    public void initialize(Map<String, Object> params) {}

                    @Override
                    public double call(String value) { return Double.parseDouble(value); }
                });
        }};

        public static final String TRANSFORMER_ID = "hex.genmodel.mojopipeline.transformers.ToNumericConversion";
        
        public static ToNumericConversionFunction getFunction(String functionName) {
            final ToNumericConversionFunction function = _supportedFunctions.get(functionName);
            if (function == null) {
                throw new UnsupportedOperationException(
                    String.format("The function '%s' is not supported conversion to numeric.", functionName));
            }
            return function;
        }
        
        public static boolean functionExists(String functionName) {
            return _supportedFunctions.containsKey(functionName);
        }

        @Override
        public String transformerName() {
            return TRANSFORMER_ID;
        }

        @Override
        public MojoTransform createBuilder(MojoFrameMeta meta,
                                           int[] iindcies, int[] oindices,
                                           Map<String, Object> params,
                                           ReaderBackend backend) {
            final String functionName = (String) params.get("function");
            final ToNumericConversionFunction function = Factory.getFunction(functionName);
            function.initialize(params);
            return new ToNumericConversion(iindcies, oindices, function);
        }
    }
}

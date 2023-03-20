package hex.genmodel.mojopipeline.transformers;

import ai.h2o.mojos.runtime.api.backend.ReaderBackend;
import ai.h2o.mojos.runtime.frame.MojoFrame;
import ai.h2o.mojos.runtime.frame.MojoFrameMeta;
import ai.h2o.mojos.runtime.transforms.MojoTransform;
import ai.h2o.mojos.runtime.transforms.MojoTransformBuilderFactory;

import java.util.HashMap;
import java.util.Map;

public class MathBinaryTransform extends MojoTransform {

    MathBinaryFunction _function;

    MathBinaryTransform(int[] iindices, int[] oindices, MathBinaryFunction function) {
        super(iindices, oindices);
        _function = function;
    }

    @Override
    public void transform(MojoFrame frame) {
        double[] left = (double[]) frame.getColumnData(iindices[0]);
        double[] right = (double[]) frame.getColumnData(iindices[1]);
        double[] o = (double[]) frame.getColumnData(oindices[0]);
        for (int i = 0, nrows = frame.getNrows(); i < nrows; i++) {
            o[i] = _function.call(left[i], right[i]);
        }
    }

   interface MathBinaryFunction {
        double call(double left, double right);
    }

    public static class Factory implements MojoTransformBuilderFactory {
        
        private static boolean isEqual(double l, double r) {
            if (Double.isNaN(l) && Double.isNaN(r)) return true;
            double ulpLeft = Math.ulp(l);
            double ulpRight = Math.ulp(r);
            double smallUlp = Math.min(ulpLeft, ulpRight);
            double absDiff = Math.abs(ulpLeft - ulpRight); // subtraction order does not matter, due to IEEE 754 spec
            return absDiff <= smallUlp;
        }

        private static double and(double l, double r) {
            return (l == 0 || r == 0) ? 0 : (Double.isNaN(l) || Double.isNaN(r) ? Double.NaN : 1);
        }
        
        private static double or(double l, double r) {
            return (l == 1 || r == 1) ? 1 : (Double.isNaN(l) || Double.isNaN(r) ? Double.NaN : 0);
        }
        
        private static final HashMap<String,MathBinaryFunction> _supportedFunctions = new HashMap<String,MathBinaryFunction>() {{
            put("round", new MathBinaryFunction() {
                @Override
                public double call(double x, double digits) {
                    if (Double.isNaN(x)) return x;
                    double sgn = x < 0 ? -1 : 1;
                    x = Math.abs(x);
                    if ((int) digits != digits) digits = Math.round(digits);
                    double power_of_10 = (int) Math.pow(10, (int) digits);
                    return sgn * (digits == 0
                            // go to the even digit
                            ? (x % 1 > 0.5 || (x % 1 == 0.5 && !(Math.floor(x) % 2 == 0)))
                            ? Math.ceil(x)
                            : Math.floor(x)
                            : Math.floor(x * power_of_10 + 0.5) / power_of_10);
                }
            });
            put("signif", new MathBinaryFunction() {
                @Override
                public double call(double x, double digits) {
                    if (Double.isNaN(x)) return x;
                    if (digits < 1) digits = 1; //mimic R's base::signif
                    if ((int) digits != digits) digits = Math.round(digits);
                    java.math.BigDecimal bd = new java.math.BigDecimal(x);
                    bd = bd.round(new java.math.MathContext((int) digits, java.math.RoundingMode.HALF_EVEN));
                    return bd.doubleValue();
                }
            });
            put("&", new MathBinaryFunction() {
                @Override
                public double call(double l, double r) {
                    return and(l, r);
                }
            });
            put("&&", new MathBinaryFunction() {
                @Override
                public double call(double l, double r) {
                    return and(l, r);
                }
            });
            put("|", new MathBinaryFunction() {
                @Override
                public double call(double l, double r) {
                    return or(l, r);
                }
            });
            put("||", new MathBinaryFunction() {
                @Override
                public double call(double l, double r) {
                    return or(l, r);
                }
            });
            put("==", new MathBinaryFunction() {
                @Override
                public double call(double l, double r) {
                    return isEqual(l, r) ? 1 : 0;
                }
            });
            put("!=", new MathBinaryFunction() {
                @Override
                public double call(double l, double r) {
                    return isEqual(l, r) ? 0 : 1;
                }
            });
            put("<=", new MathBinaryFunction() {
                @Override
                public double call(double l, double r) {
                    return l <= r ? 1 : 0;
                }
            });
            put("<", new MathBinaryFunction() {
                @Override
                public double call(double l, double r) {
                    return l < r ? 1 : 0;
                }
            });
            put(">=", new MathBinaryFunction() {
                @Override
                public double call(double l, double r) {
                    return l >= r ? 1 : 0;
                }
            });
            put(">", new MathBinaryFunction() {
                @Override
                public double call(double l, double r) {
                    return l > r ? 1 : 0;
                }
            });
            put("intDiv", new MathBinaryFunction() {
                @Override
                public double call(double l, double r) {
                    return (((int) r) == 0) ? Double.NaN : (int) l / (int) r;
                }
            });
            put("%/%", new MathBinaryFunction() {
                @Override
                public double call(double l, double r) {
                    return (int) (l / r);
                }
            });
            put("%", new MathBinaryFunction() {
                @Override
                public double call(double l, double r) {
                    return l % r;
                }
            });
            put("%%", new MathBinaryFunction() {
                @Override
                public double call(double l, double r) {
                    return l % r;
                }
            });
            put("*", new MathBinaryFunction() {
                @Override
                public double call(double l, double r) {
                    return l * r;
                }
            });
            put("/", new MathBinaryFunction() {
                @Override
                public double call(double l, double r) {
                    return l / r;
                }
            });
            put("+", new MathBinaryFunction() {
                @Override
                public double call(double l, double r) {
                    return l + r;
                }
            });
            put("-", new MathBinaryFunction() {
                @Override
                public double call(double l, double r) {
                    return l - r;
                }
            });
            put("^", new MathBinaryFunction() {
                @Override
                public double call(double l, double r) {
                    return Math.pow(l, r);
                }
            });
        }};

        public static final String TRANSFORMER_ID = "hex.genmodel.mojopipeline.transformers.MathBinaryTransform";
        
        public static MathBinaryFunction getFunction(String functionName) {
            final MathBinaryFunction function = _supportedFunctions.get(functionName);
            if (function == null) {
                throw new UnsupportedOperationException(
                        String.format("The function '%s' is not supported unary math transformation.", functionName));
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
            final MathBinaryFunction function = Factory.getFunction(functionName);
            return new MathBinaryTransform(iindcies, oindices, function);
        }
    }
}

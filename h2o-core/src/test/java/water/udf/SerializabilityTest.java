package water.udf;

import org.apache.commons.lang.SerializationUtils;
import org.junit.Test;
import water.udf.fp.Function;
import water.udf.fp.Functions;
import water.udf.fp.PureFunctions;
import water.udf.specialized.EnumColumn;
import water.udf.specialized.Enums;

import java.util.Arrays;
import java.util.Date;
import java.util.List;

import static org.junit.Assert.*;
import static water.udf.specialized.Doubles.*;
import static water.udf.specialized.Dates.*;
import static water.udf.specialized.Strings.*;

/**
 * Test for UDF
 */
public class SerializabilityTest extends UdfTestBase {

  public int requiredCloudSize() { return 1; }

  @SuppressWarnings("unchecked")
  private <T> void checkSerialization(Column<T> c) {
    byte[] serialized = SerializationUtils.serialize(c);
    Object x = SerializationUtils.deserialize(serialized);
    Column<T> copy = (Column<T>)x;
    boolean eq = c.equals(copy); // for debugging
    assertEquals(c, copy);
  }

  @Test
  public void testDoubleColumnSerializable() throws Exception {
    Column<Double> c = someDoubles();
    checkSerialization(c);
  }

  private DataColumn<Double> someDoubles() throws java.io.IOException {
    return willDrop(Doubles.newColumn(5, new Function<Long, Double>() {
      public Double apply(Long i) { return (i > 10 && i < 20) ? null : Math.sin(i); }
    }));
  }

  @Test
  @SuppressWarnings("unchecked")
  public void testDateColumnSerializable() throws Exception {
    Column<Date> c = willDrop(Dates.newColumn(7, new Function<Long, Date>() {
      public Date apply(Long i) {
        return new Date(i*3600000L*24);
      }
    }));
    checkSerialization(c);
  }

  @Test
  @SuppressWarnings("unchecked")
  public void testStringColumnSerializable() throws Exception {
    Column<String> c = willDrop(Strings.newColumn(7, new Function<Long, String>() {
      public String apply(Long i) {
        return "<<" + i + ">>";
      }
    }));
    checkSerialization(c);
  }

  @Test
  @SuppressWarnings("unchecked")
  public void testEnumColumnSerializable() throws Exception {
    Column<Integer> c = willDrop(Enums.enums(new String[]{"Red", "White", "Blue"}).newColumn(7, new Function<Long, Integer>() {
      public Integer apply(Long i) {
        return (int)(i % 3);
      }
    }));
    checkSerialization(c);
  }

  @Test
  @SuppressWarnings("unchecked")
  public void tesFunColumnSerializable() throws Exception {
    Column<Double> source = someDoubles();
    Column<Double> c = willDrop(new FunColumn<>(PureFunctions.SQUARE, source));

    checkSerialization(c);
  }

  @Test
  @SuppressWarnings("unchecked")
  public void tesFun2ColumnSerializable() throws Exception {
    Column<Double> x = someDoubles();
    Column<Double> c = willDrop(new Fun2Column<>(PureFunctions.PLUS, x, x));

    checkSerialization(c);
  }

  @Test
  @SuppressWarnings("unchecked")
  public void tesFun3ColumnSerializable() throws Exception {
    Column<Double> x = someDoubles();
    Column<Double> y = someDoubles();
    Column<Double> c = willDrop(new Fun3Column<>(PureFunctions.X2_PLUS_Y2_PLUS_Z2, x, y, x));

    checkSerialization(c);
  }

  @Test
  @SuppressWarnings("unchecked")
  public void tesFoldingSerializable() throws Exception {
    Column<Double> x = someDoubles();
    Column<Double> y = someDoubles();
    Column<Double> c = willDrop(new FoldingColumn<>(PureFunctions.SUM_OF_SQUARES, x, y, x));

    checkSerialization(c);
  }

  @Test
  @SuppressWarnings("unchecked")
  public void testUnfoldingColumnSerializable() throws Exception {
    Column<String> source1 = willDrop(Strings.newColumn(Arrays.asList("line 1; line 2; lin 3".split("; "))));

    // produce another (virtual) column that stores a list of strings as a row value
    Column<List<String>> ufc
        = new UnfoldingColumn<>(PureFunctions.splitBy(","), source1, 10);
    checkSerialization(ufc);

    EnumColumn source2 = willDrop(new Enums(new String[]{"red", "white", "blue"}).newColumn(Arrays.asList(0,1,1,0,2,2,1,2)));

    Column<List<Integer>> ohe = source2.oneHotEncode();
    checkSerialization(ohe);
  }
}

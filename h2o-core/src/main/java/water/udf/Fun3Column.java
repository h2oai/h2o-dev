package water.udf;

import water.fvec.Vec;
import water.udf.fp.Function3;
import water.udf.fp.Functions;

/**
 * This column depends on three other columns
 */
public class Fun3Column<X, Y, Z, T> extends FunColumnBase<T> {
  private final Function3<X, Y, Z, T> f;
  private final Column<X> xs;
  private final Column<Y> ys;
  private final Column<Z> zs;

  @Override public int rowLayout() { return xs.rowLayout(); }
  /**
   * deserialization :(
   */
  public Fun3Column() {
    f = null; xs = null; ys = null; zs = null;
  }

  public Fun3Column(Function3<X, Y, Z, T> f, Column<X> xs, Column<Y> ys, Column<Z> zs) {
    super(xs);
    this.f = f;
    this.xs = xs;
    this.ys = ys;
    this.zs = zs;
    assert xs.isCompatibleWith(ys) : "Columns 1 and 2 must be compatible: " + xs + ", " + ys;
    assert xs.isCompatibleWith(zs) : "Columns 1 and 3 must be compatible: " + xs + ", " + zs;
  }
  
  @Override public T get(long i) { 
    return isNA(i) ? null : f.apply(xs.apply(i), ys.apply(i), zs.apply(i)); 
  }

  @Override
  public TypedChunk<T> chunkAt(int i) {
    return new FunChunk(xs.chunkAt(i), ys.chunkAt(i), zs.chunkAt(i));
  }

  @Override public boolean isNA(long i) { return xs.isNA(i) || ys.isNA(i); }

  /**
   * Pretends to be a chunk of a column, for distributed calculations.
   * Has type, and is not materialized
   */
  public class FunChunk extends DependentChunk<T> {
    private final TypedChunk<X> cx;
    private final TypedChunk<Y> cy;
    private final TypedChunk<Z> cz;

    public FunChunk(TypedChunk<X> cx, TypedChunk<Y> cy, TypedChunk<Z> cz) {
      super(cx);
      this.cx = cx;
      this.cy = cy;
      this.cz = cz;
    }

    @Override public Vec vec() { return Fun3Column.this.vec(); }

    @Override public boolean isNA(long i) { return cx.isNA(i) || cy.isNA(i) || cz.isNA(i); }

    @Override public T get(long i) {
      return f.apply(cx.get(i), cy.get(i), cz.get(i));
    }
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (o instanceof Fun3Column) {
      Fun3Column other = (Fun3Column) o;
      return Functions.equal(f, other.f) && xs.equals(other.xs);
    }
    return false;

  }

  @Override
  public int hashCode() {
    return 61 * xs.hashCode() + Functions.hashCode(f);
  }

  @Override public String toString() { return "Fun3Column(" + f.getClass().getSimpleName() + "," + xs + "," + ys+ "," + zs + ")"; }
}

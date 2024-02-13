package water;

/**
 *  Auto-serializer interface using a delegator pattern (the faster option is
 *  to byte-code gen directly in all Iced classes, but this requires all Iced
 *  classes go through a ClassLoader).
 *  <p>
 *  Freezable is a marker interface, and {@link Iced} is the companion marker
 *  class.  Marked classes have 2-byte integer type associated with them, and
 *  an auto-genned delegate class created to actually do serialization.
 *  Serialization is extremely dense (includes various compressions), and
 *  typically memory-bandwidth bound to generate. Note that the first object implementing Freezable
 *  is the start of the serialization, serialization for parent objects is not going to be generated and user needs to provide
 *  custom serialization if that is the case.
 *  <p>
 *  H2O uses Iced classes as the primary means of moving Java Objects around
 *  the cluster.
 *  <p>
 *  Default serialization behavior can be override by user by implementing his own serialization methods. (NOTE:All custom serialization methods must be declared as either final or static!)
 *
 *  If given Freezable class contains custom serialization method, it uses it instead of the default autogenerated one (i.e. no auto-serialization happens for this class!),
 *  however, all Freezable parents are still going to be serialized automatically.
 *
 *  The serialization behavior for a given freezable class F can be described in following steps (here shown on serialization into bytes, other methods are analogical):
 *  H2O will generate F$Icer extends ((parent of F)$Icer if freezable, water.Icer otherwise).
 *
 *  F$Icer.write( F f, Autobuffer ab) {
      super.write(f,ab);
 *    // if F has custom serialization defined:
 *    return f.write_impl(ab) (or return F.write_impl(f,ab), depending on the flavor of implemented custom serialization);
 *    // otherwise auto serialize all non-static non-transient memebers of F and return ab
 *  }
 *
 *  The default serialization behavior can be overriden for given class by implementing one of or all of following custom serialization methods:
 *
 *     1) override serialization into AutoBuffer provide either
 *
 *        public final  AutoBuffer write_impl(Autobuffer ab);
 *        or
 *        public static AutoBuffer write_impl(Autobuffer ab, T t);
 *
 *     2) to override deserialization from AutoBuffer provide either
 *
 *        public final  T read_impl(Autobuffer ab);
 *        or
 *        public static T read_impl(Autobuffer ab, T t);
 *
 *     3) to override serialization into JSON provide either
 *
 *        public final AutoBuffer writeJSON_impl(Autobuffer ab);
 *        or
 *        public static AutoBuffer writeJSON_impl(Autobuffer ab, T t);
 *
 *     4) to override deserialization from JSON provide either*
 *
 *         public final  T readJSON_impl(Autobuffer ab);
 *         or
 *         public static T readJSON_impl(Autobuffer ab, T t);
 *
 *     5) override serialization into array of bytes:
 *        useful for Freezable directly supported by byte array (e.g. for memory efficiency reason), @see Chunk
 *
 *        provide @Override T byte [] asBytes()
 *
 *     6) override de-serialization from array of bytes containing exactly the bytes containing the freezable and nothing more:
 *        useful for Freezable directly supported by byte array (e.g. for memory efficiency reason), @see Chunk
 *
 *        provide @Override T reloadFromBytes(byte [] ary)
 *
 *  </p>
 *  */
public interface Freezable<T extends Freezable> extends Cloneable {

  /** Standard "write thyself into the AutoBuffer" call, using the fast Iced
   *  protocol.  Real work is in the delegate {@link Icer} classes.
   *  @param ab <code>AutoBuffer</code> to write this object to.
   *  @return Returns the original {@link AutoBuffer} for flow-coding. */
  AutoBuffer write(AutoBuffer ab);
  /** Standard "read thyself from the AutoBuffer" call, using the fast Iced protocol.  Real work
   *  is in the delegate {@link Icer} classes.
   *  @param ab <code>AutoBuffer</code> to read this object from.
   *  @return Returns a new instance of object reconstructed from AutoBuffer. */
  T read(AutoBuffer ab);
  /** Standard "write thyself into the AutoBuffer" call, using JSON.  Real work
   *  is in the delegate {@link Icer} classes.
   *  @param ab <code>AutoBuffer</code> to write this object to.
   *  @return Returns the original {@link AutoBuffer} for flow-coding. */
  AutoBuffer writeJSON(AutoBuffer ab);
  /** Standard "read thyself from the AutoBuffer" call, using JSON.  Real work
   *  is in the delegate {@link Icer} classes.
   *  @param ab <code>AutoBuffer</code> to read this object from.
   *  @return Returns an instance of object reconstructed from JSON data. */
  T readJSON(AutoBuffer ab);

  /** Returns a small dense integer, which is cluster-wide unique per-class.
   *  Useful as an array index.
   *  @return Small integer, unique per-type */
  int frozenType();
  /** Return serialized version of self as a byte array.
   *  Useful for Freezables directly supported by byte array (@see Chunk)
   *  In most cases, just use the Autobuffer version.
   *  @return serialized bytes */
  byte [] asBytes();
  /**
   * Replace yourself with deserialized version from the given bytes.
   * Useful for Freezables directly supported by byte array (@see Chunk).
   * In most cases, just use the Autobuffer version.
   * @param ary byte array containing exactly (i.e. nothing else) the serialized version of the Freezable
   * @return this freshly reloaded from the given bytes.
   * */
  T reloadFromBytes(byte [] ary);
  /** Make clone public, but without the annoying exception.
   *  @return Returns this object cloned. */
  T clone();
}

package water;


import water.api.RequestServer;
import water.api.RestApiExtension;
import water.api.SchemaServer;
import water.util.Log;

import java.util.*;

public class ExtensionManager {

  private static HashMap<String, AbstractH2OExtension> coreExtensions = new HashMap<>();
  private static HashMap<String, RestApiExtension> restApiExtensions = new HashMap<>();
  private static long registerCoreExtensionsMillis = 0;
  // Be paranoid and check that this doesn't happen twice.
  private static boolean extensionsRegistered = false;
  private static boolean restApiExtensionsRegistered = false;


  public static Collection<AbstractH2OExtension> getCoreExtensions() {
    return coreExtensions.values();
  }

  public static boolean isCoreExtensionsEnabled(String extensionName){
    return coreExtensions.get(extensionName).isEnabled();
  }

  /**
   * Register H2O extensions.
   * <p/>
   * Use SPI to find all classes that extends water.AbstractH2OExtension
   * and call H2O.addCoreExtension() for each.
   */
  public static void registerCoreExtensions() {
    if (extensionsRegistered) {
      throw H2O.fail("Extensions already registered");
    }

    long before = System.currentTimeMillis();
    ServiceLoader<AbstractH2OExtension> extensionsLoader = ServiceLoader.load(AbstractH2OExtension.class);
    for (AbstractH2OExtension ext : extensionsLoader) {
      if (ext.isEnabled()) {
        ext.init();
        coreExtensions.put(ext.getExtensionName(), ext);
      }
    }
    extensionsRegistered = true;
    registerCoreExtensionsMillis = System.currentTimeMillis() - before;
  }

  public static Collection<RestApiExtension> getRestApiExtensions(){
    return restApiExtensions.values();
  }

  private static boolean areDependantCoreExtensionsEnabled(List<String> names){
    for(String name: names){
      AbstractH2OExtension ext = coreExtensions.get(name);
      if(ext == null || !ext.isEnabled()){
        return false;
      }
    }
    return true;
  }

  /**
   * Register REST API routes.
   *
   * Use reflection to find all classes that inherit from {@link water.api.AbstractRegister}
   * and call the register() method for each.
   *
   * @param relativeResourcePath Relative path from running process working dir to find web resources.
   */
  public static void regsterRestApiExtensions() {
    if (restApiExtensionsRegistered) {
      throw H2O.fail("APIs already registered");
    }

    // Log core extension registrations here so the message is grouped in the right spot.
    for (AbstractH2OExtension e : ExtensionManager.getCoreExtensions()) {
      e.printInitialized();
    }
    Log.info("Registered " + coreExtensions.size() + " core extensions in: " + registerCoreExtensionsMillis + "ms");
    Log.info("Registered H2O core extensions: " + Arrays.toString(getCoreExtensionNames()));

    long before = System.currentTimeMillis();
    RequestServer.DummyRestApiContext dummyRestApiContext = new RequestServer.DummyRestApiContext();
    ServiceLoader<RestApiExtension> restApiExtensionLoader = ServiceLoader.load(RestApiExtension.class);
    for (RestApiExtension r : restApiExtensionLoader) {
      try {
        if(areDependantCoreExtensionsEnabled(r.getRequiredCoreExtensions())) {
          r.registerEndPoints(dummyRestApiContext);
          r.registerSchemas(dummyRestApiContext);
          restApiExtensions.put(r.getName(), r);
        }
      } catch (Exception e) {
        Log.info("Cannot register extension: " + r + ". Skipping it...");
      }
    }

    restApiExtensionsRegistered = true;

    long registerApisMillis = System.currentTimeMillis() - before;
    Log.info("Registered: " + RequestServer.numRoutes() + " REST APIs in: " + registerApisMillis + "ms");
    Log.info("Registered REST API extensions: " + Arrays.toString(ExtensionManager.getRestApiExtensionNames()));

    // Register all schemas
    SchemaServer.registerAllSchemasIfNecessary(dummyRestApiContext.getAllSchemas());
  }

  private static String[] getRestApiExtensionNames(){
    return restApiExtensions.keySet().toArray(new String[restApiExtensions.keySet().size()]);
  }

  private static String[] getCoreExtensionNames(){
    return coreExtensions.keySet().toArray(new String[coreExtensions.keySet().size()]);
  }
}

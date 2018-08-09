package hex.tree;

import hex.genmodel.algos.tree.SharedTreeNode;
import hex.genmodel.algos.tree.SharedTreeSubgraph;
import hex.schemas.TreeV3;
import water.MemoryManager;
import water.api.Handler;

import java.util.*;

/**
 * Handling requests for various model trees
 */
public class TreeHandler extends Handler {
    private static final int NO_CHILD = -1;

    public TreeV3 getTree(final int version, final TreeV3 args) {
        final SharedTreeModel model = (SharedTreeModel) args.model.key().get();
        if (model == null) throw new IllegalArgumentException("Given model does not exist: " + args.model.key().toString());
        final SharedTreeModel.SharedTreeOutput sharedTreeOutput = (SharedTreeModel.SharedTreeOutput) model._output;
        validateArgs(args, sharedTreeOutput);

        final CompressedTree auxCompressedTree = sharedTreeOutput._treeKeysAux[args.tree_number][args.tree_class].get();
        final SharedTreeSubgraph sharedTreeSubgraph = sharedTreeOutput._treeKeys[args.tree_number][args.tree_class].get()
                .toSharedTreeSubgraph(auxCompressedTree, sharedTreeOutput._names, sharedTreeOutput._domains);

        final TreeProperties treeProperties = convertSharedTreeSubgraph(sharedTreeSubgraph);

        args.left_children = treeProperties._leftChildren;
        args.right_children = treeProperties._rightChildren;
        args.descriptions = treeProperties._descriptions;
        args.root_node_id = sharedTreeSubgraph.rootNode.getNodeNumber();
        args.thresholds = treeProperties._thresholds;
        args.features = treeProperties.features;
        args.nas = treeProperties.nas;

        return args;
    }


    /**
     * @param args An instance of {@link TreeV3} input arguments to validate
     * @param output An instance of {@link hex.tree.SharedTreeModel.SharedTreeOutput} to validate input arguments against
     */
    private void validateArgs(TreeV3 args, SharedTreeModel.SharedTreeOutput output) {
        if (args.tree_number < 0) throw new IllegalArgumentException("Tree number must be greater than 0.");
        if (args.tree_class < 0) throw new IllegalArgumentException("Tree class must be greater than 0.");

        if (args.tree_number > output._treeKeys.length - 1)
            throw new IllegalArgumentException("There is no such tree.");
        if (args.tree_class > output._treeKeys[args.tree_number].length - 1)
            throw new IllegalArgumentException("There is no such tree class.");
    }


    /**
     * Converts H2O-3's internal representation of a boosted tree in a form of {@link SharedTreeSubgraph} to a format
     * expected by H2O clients.
     *
     * @param sharedTreeSubgraph An instance of {@link SharedTreeSubgraph} to convert
     * @return An instance of {@link TreeProperties} with some attributes possibly empty if suitable. Never null.
     */
    static TreeProperties convertSharedTreeSubgraph(final SharedTreeSubgraph sharedTreeSubgraph) {
        Objects.requireNonNull(sharedTreeSubgraph);

        final TreeProperties treeprops = new TreeProperties();

        treeprops._leftChildren = MemoryManager.malloc4(sharedTreeSubgraph.nodesArray.size());
        treeprops._rightChildren = MemoryManager.malloc4(sharedTreeSubgraph.nodesArray.size());
        treeprops._descriptions = new String[sharedTreeSubgraph.nodesArray.size()];
        treeprops._thresholds = MemoryManager.malloc4f(sharedTreeSubgraph.nodesArray.size());
        treeprops.features = new String[sharedTreeSubgraph.nodesArray.size()];
        treeprops.nas = MemoryManager.mallocZ(sharedTreeSubgraph.nodesArray.size());

        // Set root node's children, there is no guarantee the root node will be number 0
        treeprops._rightChildren[0] = sharedTreeSubgraph.rootNode.getRightChild() != null ? sharedTreeSubgraph.rootNode.getRightChild().getNodeNumber() : -1;
        treeprops._leftChildren[0] = sharedTreeSubgraph.rootNode.getLeftChild() != null ? sharedTreeSubgraph.rootNode.getLeftChild().getNodeNumber() : -1;

        List<SharedTreeNode> nodesToTraverse = new ArrayList<>();
        nodesToTraverse.add(sharedTreeSubgraph.rootNode);
        append(treeprops._rightChildren, treeprops._leftChildren,
                treeprops._descriptions, treeprops._thresholds, treeprops.features, treeprops.nas,
                nodesToTraverse, -1, false);

        return treeprops;
    }

    private static void append(final int[] rightChildren, final int[] leftChildren, final String[] nodesDescriptions,
                               final float[] thresholds, final String[] splitColumns, final boolean[] naHandlings,
                               List<SharedTreeNode> nodesToTraverse, int pointer, boolean visitedRoot) {
        if(nodesToTraverse.isEmpty()) return;

        List<SharedTreeNode> discoveredNodes = new ArrayList<>();

        for (SharedTreeNode node : nodesToTraverse) {
            pointer++;
            final SharedTreeNode leftChild = node.getLeftChild();
            final SharedTreeNode rightChild = node.getRightChild();
            if(visitedRoot){
                fillnodeDescriptions(node, nodesDescriptions, thresholds, splitColumns, naHandlings, pointer);
            } else {
                nodesDescriptions[pointer] = "Root node";
                visitedRoot = true;
            }

            if (leftChild != null) {
                discoveredNodes.add(leftChild);
                leftChildren[pointer] = leftChild.getNodeNumber();
            } else {
                leftChildren[pointer] = NO_CHILD;
            }

            if (rightChild != null) {
                discoveredNodes.add(rightChild);
                rightChildren[pointer] = rightChild.getNodeNumber();
            } else {
                rightChildren[pointer] = NO_CHILD;
            }
        }

        append(rightChildren, leftChildren, nodesDescriptions, thresholds, splitColumns, naHandlings,
                discoveredNodes, pointer, true);
    }

    private static void fillnodeDescriptions(final SharedTreeNode node, final String[] nodeDescriptions,
                                             final float[] thresholds, final String[] splitColumns,
                                             final boolean[] naHandlings, final int pointer) {
        final StringBuilder nodeDescriptionBuilder = new StringBuilder();

        if (!Float.isNaN(node.getParent().getSplitValue())) {
            nodeDescriptionBuilder.append(node.getParent().getColName());
            if (node.isLeftward()) {
                nodeDescriptionBuilder.append(" < ");
            } else {
                nodeDescriptionBuilder.append(" >= ");
            }
            nodeDescriptionBuilder.append(node.getParent().getSplitValue());
            thresholds[pointer] = node.getParent().getSplitValue();
        } else {
            final BitSet childInclusiveLevels = node.getInclusiveLevels();
            final int cardinality = childInclusiveLevels.cardinality();
            if ((cardinality > 0)) {
                nodeDescriptionBuilder.append("Split column [");
                nodeDescriptionBuilder.append(node.getParent().getColName());
                nodeDescriptionBuilder.append("]: ");
                int bitsignCounter = 0;
                for (int i = childInclusiveLevels.nextSetBit(0); i >= 0; i = childInclusiveLevels.nextSetBit(i + 1)) {
                    nodeDescriptionBuilder.append(node.getParent().getDomainValues()[i]);
                    if (bitsignCounter != cardinality - 1) nodeDescriptionBuilder.append(", ");
                    bitsignCounter++;
                }
            }
        }

        nodeDescriptions[pointer] = nodeDescriptionBuilder.toString();
        splitColumns[pointer] = node.getParent().getColName();
        naHandlings[pointer] = node.getInclusiveNa();

    }

    public static class TreeProperties {

        public int[] _leftChildren;
        public int[] _rightChildren;
        public String[] _descriptions; // General node description, most likely to contain serialized threshold or inclusive dom. levels
        public float[] _thresholds;
        public String[] features;
        public boolean[] nas;

    }
}

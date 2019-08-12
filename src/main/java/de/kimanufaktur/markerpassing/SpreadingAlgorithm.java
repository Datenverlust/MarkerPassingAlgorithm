package de.kimanufaktur.markerpassing;

import java.util.Collection;

/**
 * Main algorithm.
 * This is the main algorithm which can be extended by implementing the different parts.
 */
public class SpreadingAlgorithm {

    //members
    private boolean terminate;
    private InFunction in;
    private OutFunction out;
    private SelectFiringNodesFunction selectFiringNodes;
    private TerminationCondition terminationCondition;
    private Collection<ProcessingStep> preprocessingSteps;
    private Collection<ProcessingStep> postprocessingSteps;
    private Collection<Node> firingNodes;
    private Collection<Node> activeNodes;

    public boolean isTerminate() {
        return terminate;
    }

    public void setTerminate(boolean terminate) {
        this.terminate = terminate;
    }

    public InFunction getIn() {
        return in;
    }

    public void setIn(InFunction in) {
        this.in = in;
    }

    public OutFunction getOut() {
        return out;
    }

    public void setOut(OutFunction out) {
        this.out = out;
    }

    public SelectFiringNodesFunction getSelectFiringNodes() {
        return selectFiringNodes;
    }

    public void setSelectFiringNodes(SelectFiringNodesFunction selectFiringNodes) {
        this.selectFiringNodes = selectFiringNodes;
    }

    public TerminationCondition getTerminationCondition() {
        return terminationCondition;
    }

    public void setTerminationCondition(TerminationCondition terminationCondition) {
        this.terminationCondition = terminationCondition;
    }

    public Collection<ProcessingStep> getPreprocessingSteps() {
        return preprocessingSteps;
    }

    public void setPreprocessingSteps(Collection<ProcessingStep> preprocessingSteps) {
        this.preprocessingSteps = preprocessingSteps;
    }

    public Collection<ProcessingStep> getPostprocessingSteps() {
        return postprocessingSteps;
    }

    public void setPostprocessingSteps(Collection<ProcessingStep> postprocessingSteps) {
        this.postprocessingSteps = postprocessingSteps;
    }

    public Collection<Node> getFiringNodes() {
        return firingNodes;
    }

    public void setFiringNodes(Collection<Node> firingNodes) {
        this.firingNodes = firingNodes;
    }

    public Collection<Node> getActiveNodes() {
        return activeNodes;
    }

    public void setActiveNodes(Collection<Node> activeNodes) {
        this.activeNodes = activeNodes;
    }

    public void execute() {
        terminate = false;
        while (!terminate) {
            pulse();
        }
    }

    /**
     * A pulse is the spreading of one iteration of activation thought a selected set of nodes.
     */
    private Collection<Node>  pulse() {
        preprocess();
        firingNodes = selectFiringNodes.compute(activeNodes);
        spread();
        postprocess();
        checkTermination();
        return activeNodes;
    }

    /**
     * The prpocessing step executed before each pulse
     */
    private void preprocess() {
        for (ProcessingStep step : preprocessingSteps) {
            step.execute();
        }
    }


    /**
     * The spreading step, which activates each node of the firingNodes.
     * @return the result of the activation set.
     */
    private void spread() {
        SpreadedMarkers spreadedMarkers = new SpreadedMarkers();
        for (Node node : firingNodes) {
            spreadedMarkers.addAll(out.compute(node));
        }
        firingNodes.clear();
        for (Node targetNode : spreadedMarkers.getTargetNodes()) {
            in.compute(spreadedMarkers.getInputForTarget(targetNode), targetNode);
            this.getActiveNodes().add(targetNode);
        }
    }

    private void postprocess() {
        for (ProcessingStep step : postprocessingSteps) {
            step.execute();
        }
    }

    private void checkTermination() {
        terminate = terminationCondition.compute();
    }

}

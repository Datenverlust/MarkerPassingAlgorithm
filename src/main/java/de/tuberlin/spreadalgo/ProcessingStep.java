package de.tuberlin.spreadalgo;

/**
 * This interface is to be implemented by the processing step done in the pre- and post-processing.
 * Since we do not want to commit to any normalization or decay strategy, the processingSetp can be
 * every task to be done with the activated network bevore and after activation.
 */
public interface ProcessingStep {

	/**
	 * The execute method is the starting point of which is called when the processing step is
	 * invoked by the Marker Passing algorithm.
	 */
	public void execute();

}

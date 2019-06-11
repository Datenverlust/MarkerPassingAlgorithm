package de.tuberlin.spreadalgo;

import java.util.Collection;

/**
 * The Out-Function defines how markers are passed to edges (links) if a node is activated.
 * This might include a weighting or a decision to which edges to pass markers to, or which information to add to the marker.
 */
public interface OutFunction {

	Collection<SpreadingStep> compute(Node node);

}

package de.kimanufaktur.spreadalgo;

import java.util.Collection;

/**
 * The In-Function processes the markers passed to a node. The In-Function thus controlled what happens to the nodes
 * before they are processed by a threshold.
 */
public interface InFunction {

	void compute(Collection<SpreadingStep> input, Node node);

}

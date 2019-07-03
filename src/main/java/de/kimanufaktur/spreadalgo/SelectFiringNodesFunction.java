package de.kimanufaktur.spreadalgo;

import java.util.Collection;

/**
 * Created by faehndrich on 06.05.15.
 */

/**
 * Function to select the size of the next pulse. Thus here we decide which nodes get to fire in the next round.
 * A standard implementation of spreading activation is, that all active nodes will fire in the next pulse.
 */
public interface SelectFiringNodesFunction {
    /**
     * Compute the firing nodes for the next pulse.
     * @param activeNodes the List of active nodes, which could become firing nodes for the next pulse
     * @return the list of firing nodes which spread in the next pulse.
     */
    Collection<Node> compute(Collection<Node> activeNodes);
}

package de.kimanufaktur.markerpassing;

import java.util.Collection;
import java.util.HashMap;
import java.util.LinkedList;

/**
 * Created by faehndrich on 06.05.15.
 * The spreaded markers are the markers which have to be handled during the spreading step.
 * This means they have been passed by some node, and need to be processes by some target node.
 */
public class SpreadedMarkers {
    HashMap<Node, Collection<SpreadingStep>> markers = new HashMap<Node, Collection<SpreadingStep>>();

    public void addAll(Collection<SpreadingStep> data) {
        for(SpreadingStep step : data) {
            Node target = step.getTargetNode();
            getInputForTarget(target).add(step);
        }
    }

    public Collection<Node> getTargetNodes() {
        return markers.keySet();
    }

    public Collection<SpreadingStep> getInputForTarget(Node targetNode) {
        Collection<SpreadingStep> ret = markers.get(targetNode);
        if(ret == null) {
            ret = new LinkedList<SpreadingStep>();
            markers.put(targetNode,ret);
        }
        return ret;
    }
}

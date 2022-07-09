package de.kimanufaktur.markerpassing;

import java.util.Collection;

/**
 * The node represents the vertex to the edges in the graph. A node holds the markers passed to it. It can be the target or the source oa a link.
 */
public interface Node {

    //Link for the network created out of nodes
    default void addLink(Link link) {
        getLinks().add(link);
    }

    default void removeLink(Link link) {
        getLinks().remove(link);
    }

    Collection<Link> getLinks();

    //de.kimanufaktur.markerpassing.Marker holding the activation information of the node
    default void addMarker(Marker marker) {
        getMarkers().add(marker);
    }

    default void removeMarker(Marker marker) {
        getMarkers().remove(marker);
    }

    Collection<Marker> getMarkers();

    //de.kimanufaktur.markerpassing.Node management functions

    /**
     * Check the Threshold of the node. If the threshold is exceeded, the node is added to the active nodes and can
     * be selected for firing.
     *
     * @param markerClasses the markers to check the threshold for.
     * @return boolean if one of the threshold is reached
     */
    boolean checkThresholds(Object markerClasses);
}


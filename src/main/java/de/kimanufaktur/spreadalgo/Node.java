package de.kimanufaktur.spreadalgo;

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

    //Marker holding the activation information of the node
    default void addMarker(Marker marker) {
        getMarkers().add(marker);
    }

    default void removeMarker(Marker marker) {
        getMarkers().remove(marker);
    }

    Collection<Marker> getMarkers();

    //Node management functions

    /**
     * Check the chreshold of the node. If the threshold is exceeded, the node is added to the active nodes and can
     * be selected for firing.
     *
     * @param markerClasses the markers to check the threshold for.
     */
    boolean checkThresholds(Object markerClasses);
}


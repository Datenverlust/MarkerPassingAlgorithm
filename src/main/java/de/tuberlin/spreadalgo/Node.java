package de.tuberlin.spreadalgo;

import java.util.Collection;

public interface Node {

    //Link for the network created out of nodes
    Collection<Link> links = null;
    public void addLink(Link link);
    public void removeLink(Link link);
    public Collection<Link> getLinks();

    //Marker holding the activation information of the node
    Collection<Marker> markers = null;
    public Collection<Marker> getMarkers();
    public void addMarker(Marker marker);
    public void removeMarker(Marker marker);

    //Node management functions

    /**
     * Check the chreshold of the node. If the threshold is exceeded, the node is added to the active nodes and can
     * be selected for firing.
     * @param markerClasses the markers to check the threshold for.
     */
    public boolean checkThresholds(Object markerClasses);
}

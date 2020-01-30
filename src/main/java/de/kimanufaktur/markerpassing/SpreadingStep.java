package de.kimanufaktur.markerpassing;

import java.util.ArrayList;
import java.util.Collection;

/**
 * This class represents one activation step which is part of the activation pulse. Earch step is the activation of one
 * link with a set of markers. It is seen as the product of an out-function. A out-function might create multiple activation
 * steps, since multiple links of a node might be activated and each link is seen as a step with an individual set of markers
 * and a target.
 * Created by faehndrich on 06.05.15.
 */
public class SpreadingStep {
    Link link = null;
    boolean inDirection;
    Collection<Marker> markings = new ArrayList<Marker>();
    public Link getLink() {
        return link;
    }

    public void setLink(Link link) {
        this.link = link;
    }

    public boolean isInDirection() {
        return inDirection;
    }

    public void setInDirection(boolean inDirection) {
        this.inDirection = inDirection;
    }

    public Collection<Marker> getMarkings() {
        return markings;
    }

    public void setMarkings(Collection<Marker> markings) {
        this.markings = markings;
    }


    public Node getTargetNode(){
        if(link == null){
            //TODO: error handling

            return null;
        }
        Node result = null;
        if(inDirection){
            result = getLink().getTarget();
        }else{
            result = getLink().getSource();
        }
        return result;
    }

    }

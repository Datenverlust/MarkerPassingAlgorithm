package de.kimanufaktur.spreadalgo;

/**
 * Created by faehndrich on 06.05.15.
 */

/**
 * The link interface represents the edges of the graph. It is a directed edge with source and traget.
 * TODO: Here the generalization to multiple source and targets is missing.
 */
public interface Link {
    Node getSource();
    void setSource(Node source);
    Node getTarget();
    void setTarget(Node target);

}

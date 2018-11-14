package de.tuberlin.spreadalgo;

/**
 * Created by faehndrich on 06.05.15.
 */
public interface Link {
    Node getSource();
    void setSource(Node source);
    Node getTarget();
    void setTarget(Node target);

}

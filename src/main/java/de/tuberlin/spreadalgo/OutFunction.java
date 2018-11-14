package de.tuberlin.spreadalgo;

import java.util.Collection;

public interface OutFunction {

	Collection<SpreadingStep> compute(Node node);

}

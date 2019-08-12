package de.kimanufaktur.markerpassing;


/**
 * The termination condition is used to evaluate of another spreding step should be made.
 * This shout evaluate to true if the algorithm should terminate.
 */
public interface TerminationCondition {

	boolean compute();

}

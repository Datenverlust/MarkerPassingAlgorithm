# MarkerPassingAlgorithm
This is an generalized implementation of the general Marker Passing algorithm published by: Crestani (https://doi.org/10.1023/A:1006569829653).
The idea is the same as in activation spreading (for more details you can start here: https://en.wikipedia.org/wiki/Spreading_activation), but the implementation is more general. 
Marker Passing extends the "double value" which is used in spreading activation as activation or zorch to a general marker.
This marker can contain all information wanted. It is passt to other nodes, which can modify this marker. 
With this algorithm, we can subsum some simple models like PetriNets and some more complex Models Like ANN. 

But the here proposed algorithm can do way more. Your imagination is the limit.

# FullStack
The idea is quite simple: Input is a graph, which is used as basis for the marker passing. A set of start markers on the graph is the initial configuration and  a Termination conditions which terminates the algorithm.
Additionally the implementation of the general marker passing is done by specifying a "Node Interpretation". This includes the activation function, and many more optoins to specify how the markers are passed over the given graph. 

[For further questions you can contact me on Twitter](https://twitter.com/Datenverlust) 

![Algorithenm](http://fähndrich.de/images/Faehndrich2018.png)

A application of this algorithm can be found in the following paper:
```sh
@InProceedings{Faehndrich2018,
author="F{\"a}hndrich, Johannes
and Weber, Sabine
and Kanthak, Hannes",
editor="Ichise, Ryutaro
and Lecue, Freddy
and Kawamura, Takahiro
and Zhao, Dongyan
and Muggleton, Stephen
and Kozaki, Kouji",
title="A Marker Passing Approach to Winograd Schemas",
booktitle="Semantic Technology",
year="2018",
publisher="Springer International Publishing",
address="Cham",
pages="165--181",
abstract="This paper approaches a solution of Winograd Schemas with a marker passing algorithm which operates on an automatically generated semantic graph. The semantic graph contains common sense facts from data sources form the semantic web like domain ontologies e.g. from Linked Open Data (LOD), WordNet, Wikidata, and ConceptNet. Out of those facts, a semantic decomposition algorithm selects relevant facts for the concepts used in the Winograd Schema and adds them to the semantic graph. Markers are propagated through the graph and used to identify an answer to the Winograd Schema. Depending on the encoded knowledge in the graph (connectionist view of world knowledge) and the information encoded on the marker (for symbolic reasoning) our approach selects the answers. With this selection, the marker passing approach is able to beat the state-of-the-art approach by about 12{\%}.",
isbn="978-3-030-04284-4"
}
```


## What is this?
This project is an first try of an implementation of such an general marker passing algorithm. You might want to extend it to use less boiler plate code. 
The ides is that we collect example implementations here and perhaps improve the representation of the used graph or markers. 
So please feel free to contributed with any example, test or improvment idea. 

## Other cool things

We have implemented some examples using this algorithm with some success. You can finde the papers here: www.fähndrich.de


## Usage

Soon there will be examples here.


```sh
# Run marker passing test

```

## License

[GPLv3](https://www.gnu.org/licenses/gpl-3.0.html)
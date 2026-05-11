Presented to Coleman, Mason, Evan

# Overview
This project's goal is to create a fullstack web app that interfaces with a finetuned small language model (the Llama 3.2-3B) trained on a large amount of marimba mallet descriptions and the Leigh Howard Stevens book *Method of Movement* but also hooked up to a RAG database. The model should be able to (at least somewhat) accurately answer questions surrounding marimba methodology and mallet differences. 

We used playwright to scrape the Steve Weiss website (an online percussion equipment store) for marimba mallet names, model number, and description to create a large marimba dataset. After collecting the data, we use Google Gemini's model to create queries from the mallet database and the method of movement book.We also use Chromadb for a vectordatabase for our RAG implementation. 

Our webscraping, query creation, and fine-tuning is all done within a Google colab notebook while our backend is written in Python and frontend in React. 

# RAG Implementation Testing
To test our language model we did some searching and came across the RAG Implementation testing method of [RAG Triad](https://www.trulens.org/getting_started/core_concepts/rag_triad/) and *LLM-As-A-Judge* evaluation pipelines. We created a small 'golden dataset' of marimba pedagogy questions covering technique, equipment, and repertoire. The evaluation queried the local backend api and then submitted the retrieved context alongside the model's generated answers to Gemini 2.5 Pro to grade. 

The evaluator model (Gemini) measures two primary metrics on a strict 0.0 to 1.0 scale -
- **Contextual Accuracy:** how factually correct/complete the answer is related to the retrieved context
- **Groudedness:** the faithfulness of the generation to the retrieved sources (measuring the absence of hallucination and/or outside extrapolation)

**Results:**
| Metric | Average Score | Description |
| :--- | :--- | :--- |
| **Contextual Accuracy** | **32.50%** | Adherence to the specific details in the retrieved text. |
| **Groundedness** | **45.00%** | Percentage of generated claims directly supported by the retrieved chunks. |

While these results aren't exactly great, we need to consider many things:
1. Our local model is only a 3B model that could be fine-tuned on accessible hardware in only about ~40 minutes. Hallucination was and is almost guarunteed even after fine-tuning. A 3B model will also struggle to integrate dense instructional context without generalizing, making these results make a lot more sense.
2. This process of testing our model is specifically looking at our RAG implementation. As we've already fine-tuned the model on relevant topics but we're measuring groudedness which penalizes the model on generating any content outside of the retrieved chunks, often the model is at least somewhat correct in its answer but it got its context not from the rag implementation and instead from its finetuning.
3. Looking at the `eval_results.json` file we can see our embedding model (`BAAI/bge-base-en-v1.5`) will retrieve overlapping or incomplete chunks from pdfs/documents. If the chunk cuts off mid explanation, our local model is forced to extrapolate which may drop the overall accuracy of the answer.
4. Our golden dataset is small and we only performed one pass of this test on the model without optimizing anything. If we continue working I'm confident we could get our rag implementation's accuracy up.

# Model Comparison
We didn't do any formal comparisons between the base Llama model, our fine-tuned model, and the fine-tuned + rag model. However we did informally ask all three model versions the same question to compare their answers. 

The base model did seem to have some musical knowledge but didn't really understand what we were asking and would confuse specific equipment together. For example it began recommending drumstick styles rather than marimba mallets. It also gave quite lengthy answers without having anything very meaningful in the answer.

Our fine-tuned model performed better and typically gave real mallet names. However in pedagogical questions it would often hallucinate names of people who created certain techniques. Overall its vocabulary was much more appropriate and more specific for the questions asked but still lacked the very specific names/knowledge it had been trained on at times.

The RAG implementation fixed this issue with our trained model. Combining RAG with fine-tuning gave us the most consistently correct (or at least somewhat correct) answers of the three models. It gave specific model names and knew more about the materials of the mallets. However it still would sometimes hallucinate and come up with contradictory answers. This is almost certainly due to the smaller model we chose and could probably be improved by changing models.

*An example question and the models' responses is shown below.*

**Test Question:** *I’m playing a lyrical solo on a rosewood marimba and need something for the middle register. What IP mallet do you recommend?*

```
Base Model Answer:
For a lyrical solo on a rosewood marimba, I'd recommend using a mallet with a medium to medium-hard feel to provide a clear, articulate sound and a sense of clarity in the middle register.

In this range, I'd suggest using a mallet with a medium to medium-hard tip size, such as:

* 5A or 5B for a more mellow, warm sound
* 5C or 5D for a slightly brighter, more defined sound

Avoid using very hard mallets (like 5E or 5F) as they can produce a harsh, overpowered sound that may not be suitable for a lyrical solo.

Additionally, consider using a mallet with a medium to medium-hard tip material, such as:

* Nylon or nylon-wrapped mallets (e.g., ProMark or Vic Firth) for a warm, balanced sound
* Synthetic mallets (e.g., ProMark or Vater) for a bright, crisp sound

Avoid using very soft mallets (like 1A or 1B) as they may not provide enough power and definition for a lyrical solo.

Remember, the key is to find a balance between power
```

```
Trained Model Answer:
For a rosewood marimba and a lyrical solo in the middle register, I'd highly recommend the Innovative Percussion IP310. Its medium-hardness and balanced core will provide a warm, full sound with good articulation, making it perfect for expressive passages.
```

```
RAG and Trained Model Answer:
Based on your description of needing something for the middle register on a rosewood marimba for a lyrical solo, I would highly recommend the Innovative Percussion IP400 Soloist Series Hard Marimba Mallets. Their 100% wool yarn and hard rubber cores are specifically designed to produce a full, rich tone and warm fundamental, which will complement the rosewood beautifully and allow for the expressive qualities you're looking for in that middle register. The IP400's articulation is also designed to be strong, which will help you achieve the clarity and projection you need for a solo performance. While the IP240 and IP275 are also excellent choices, the IP400's focus on the upper 3 octaves and its articulation profile make it the best fit for your specific needs.
```

# Conclusion
We learned a lot in this project and was able to combine a lot of what we'd learned in class. It was interesting getting to play around with dataset creation using webscraping and integrate LLMs like Gemini in our project. Also looking into different types of model testing frameworks like RAG Triad was intersting and helpful. 

Though our model didn't perform extremely accurately the fact that we were able to complete this project in a relatively short amount of time and still get coherent, somewhat accruate answers is fairly impressive. Now we understand and know how to finetune models and can apply this knowledge to larger models with with better data, we know of a framework to test RAG implementation, and we understand more about vector databases like ChromaDB.

If we were to continue on this project adding an alignment aspect to it would be very interesting, as some questions it was clear it had no knowledge on but would still try to force it back to something it did know (like when asking "Why's the sky blue?" it would then bring up a mallet that's color is 'sky-blue'). Upgrading to a larger model and also going into the querries and verifying training querries/data would be another step we could/should take if we were to continue work on it. Overall though for a first fine-tuning attempt, we were both happy with the model's performance, especially once hooked up with RAG in terms of answer accuracy. 

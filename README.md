# GPT2 Superheroes

[![Run on Ainize](https://ainize.ai/images/run_on_ainize_button.svg)](https://ainize.web.app/redirect?git_repo=https://github.com/fpem123/GPT2-Superheroes)

This project generate Superhero story and power using GPT-2 model.

Fine tuning data: [Kaggle](https://www.kaggle.com/jonathanbesomi/superheroes-nlp-dataset)

### Model information

* Superhero story model


    Base model: gpt-2 large
    Epoch: 30
    Train runtime: 6865.2586 secs
    Loss: 0.0278


* Superhero power model


    Base model: gpt-2 large
    Epoch: 30
    Train runtime: 2142.469 secs
    Loss: 0.0185


### How to use

    * First, Fill what the text. This will be base of story and power.
    * And then, Fill number in length. Text is created as long as "length". I recommend between 100 and 300.
    * If length is so big, generate time will be long.

### Post parameter

    text: Base text for generate
    length: The size of generated text.


### Output format

    {"0": generated text}


## * With CLI *

### Input example

* Hero's Story


    curl -X POST "https://master-gpt2-superheroes-fpem123.endpoint.ainize.ai/superhero/story" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "text=superman is" -F "length=50"


* Hero's Power


    curl -X POST "https://master-gpt2-superheroes-fpem123.endpoint.ainize.ai/superhero/power" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "text=Superman is" -F "length=50"


### Output example

Hero's Story


    {
        "0": "Superman is resurrected and finds his way back to Metropolis. Superman tracks down Superboy and takes him to the Fortress of Solitude. He tries to make him stop but is unable. Superboy-Prime goes on the attack, but Superman is able to keep"
    }

Hero's Power 

  
    {
        "0": "Superman is able to generate great amounts of physical force through kinetic energy, simulating superhuman strength, even in a stationary position. This \"free-running\" ability allows him to move at speeds much faster than a normal human. He can use this speed to attack"
    }


## * With swagger *

API page: [Ainize](https://ainize.ai/fpem123/GPT2-Superheroes?branch=master)

## * With a Demo *

Demo page: [End-point](https://master-gpt2-superheroes-fpem123.endpoint.ainize.ai/)
from OpenAI_services import generaRisposta
#Main    : Establish connection with Arduino
#THREAD 1: Wait for wakeword -> Mic input on azure STT -> OpenAI API call -> Azure TTS output on speaker
#THREAD 2: Read distance values from Arduino -> Move accordingly (either following line or idling)
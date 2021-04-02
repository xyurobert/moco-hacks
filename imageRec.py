##############################################################################
# Installation
##############################################################################


##############################################################################
# Initialize client
##############################################################################

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_pb2, status_code_pb2

channel = ClarifaiChannel.get_grpc_channel()

# Note: You can also use a secure (encrypted) ClarifaiChannel.get_grpc_channel() however
# it is currently not possible to use it with the latest gRPC version

stub = service_pb2_grpc.V2Stub(channel)

# This will be used by every Clarifai endpoint call.
metadata = (('authorization', 'Key d9f3e694528f43c3940c70a386e1ccf4'),)

imageURL = ["https://c.saavncdn.com/979/Harley-Dean-English-2018-20180322045950-500x500.jpg"]

# "https://images2.minutemediacdn.com/image/upload/c_fill,g_auto,h_1248,w_2220/v1555922701/shape/mentalfloss/istock_000008977856_small.jpg?itok=LB1PV-vj" , "https://ci-ph.rdtcdn.com/m=eQdw9f/pics/pornstars/000/053/022/thumb_1176621.jpg"

def imageIsProfane(imageURL): #note,imageList is an object and you would need to call the image url
    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            model_id="d16f390eb32cad478c7ae150069bd2c6",
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        image=resources_pb2.Image(
                            url= imageURL
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )
    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

    # Since we have one input, one output will exist here.
    output = post_model_outputs_response.outputs[0]

    #print("Predicted concepts:")
    #safeList = []
    for concept in output.data.concepts:
        
        #score = "%.2f" % (concept.value)
        #safeList.append(score)
        #print("%s %.2f" % (concept.name, concept.value))
        if str(concept.name) == 'safe':
            if concept.value < 0.8:
                print('Flagged: NSFW')
                return True #nsfw
            print('Not Flagged: SFW')
            return False
                #imageURL is the JSON Object, and you would add the post ID to the list and not the image URL
    #print(safeL

# print(filterImage("https://c.saavncdn.com/979/Harley-Dean-English-2018-20180322045950-500x500.jpg")) #use for loop to append tweet IDS to the flagged tweet list in profanityFilter. In profanity filter you would compare lists and remove duplicates
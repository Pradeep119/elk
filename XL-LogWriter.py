import threading
import time
import datetime
import multiprocessing
import random
import uuid

 

# can change tps sps and apis count
tps = 50
sps = 10
apis = 10

 

mintt = 100000
loopval = tps
loopval = 400

 

API_REQUEST_ID = 0
BODY = "< soapenv: Body xmlns: soapenv = http://schemas.xmlsoap.org/soap/envelope/ > < jsonObject > < " \
       "requestError > < policyException > < messageId > POL1000 < / messageId > < text > User has insufficient " \
       "credit for transaction. </ text > < variable > NotEnoughCredit < / variable > < / policyException > < / " \
       "requestError > < / jsonObject > < / soapenv:Body > "

 

REQUESTBODY = "<soapenv:Body xmlns:soapenv=http://schemas.xmlsoap.org/soap/envelope/><jsonObject><amountTransaction" \
              "><endUserId>acr:OrangeAPIToken</endUserId><paymentAmount><chargingInformation><description>Abonnement " \
              ">100</totalAmountCharged><chargingMetaData><onBehalfOf>DEUXPOINTZERO-AFRIPULSE</onBehalfOf><serviceId" \
              ">BIZAO</serviceId></chargingMetaData></paymentAmount><transactionOperationStatus>Charged" \
              "</transactionOperationStatus><referenceCode>PDKSUB|22577242881|23_08_19_00_03</referenceCode" \
              "></amountTransaction></jsonObject></soapenv:Body> "

 

RESPONSEBOSY = "<soapenv:Body xmlns:soapenv=http://schemas.xmlsoap.org/soap/envelope/><jsonObject><requestError" \
               "><policyException><messageId>POL1000</messageId><text>User has insufficient credit for " \
               "></soapenv:Body> "

 

API_NAME_LIST = ["API{:02d}".format(x) for x in range(apis)]
SP_NAME_LIST = ["xl@carbon.super{:02d}".format(x) for x in range(sps)]
SP_NAME_LIST.append("admin")
HTTP_STATUS_LIST = [200, 201, 403, 302]

 


def getRequestData():
    global API_REQUEST_ID

 

    DATETIME = str(datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3])
    TRANSACTION = "request"
    API_REQUEST_ID = "urn:uuid:" + str(uuid.uuid1())
    API_NAME = random.choice(API_NAME_LIST)
    SP_NAME = random.choice(SP_NAME_LIST)
    API_PUBLISHER = "admin"
    API_VERSION = "v1"
    API_CONTEXT = "/ payment / v1"
    APPLICATION_NAME = "Deuxpointzero - appli01"
    APPLICATION_ID = "142"
    CONSUMER_KEY = "N2xe7KTpLxzk25FZEnS0YgmlD10a"
    API_RESOURCE_PATH = "/acr%3AOrangeAPIToken/transactions/amount"
    METHOD = "POST"
    BIZAO_TOKEN = "B64vysAfYC + aQ1uAgo97yHXxj1vVVE5L4YQWvz / gWPXb5RSPiFAQCocBabb6GXtn58r | MCO = OCI | tcd = " \
                  "1563407971 | BZvRGPq0vrXu2 + E6CNtU071cCpU = "
    BIZAO_ALIAS = "PDKSUB - 200 - yWGUWx4xdPtIPLgWdLdri8G + yf86s8DRejZsb24sPsc "

 

    val = " [" + DATETIME + "]" + "  INFO {REQUEST_RESPONSE_LOGGER} -  TRANSACTION:" + TRANSACTION + ",API_REQUEST_ID:" + API_REQUEST_ID + ",API_NAME:" + API_NAME + ",SP_NAME:" + SP_NAME + ",API_PUBLISHER:" + API_PUBLISHER + ",API_VERSION:" + API_VERSION + ",API_CONTEXT:" + API_CONTEXT + ",APPLICATION_NAME:" + APPLICATION_NAME + ",APPLICATION_ID:" + APPLICATION_ID + ",CONSUMER_KEY:" + CONSUMER_KEY + ",API_RESOURCE_PATH:" + API_RESOURCE_PATH + ",METHOD:" + METHOD + ",BODY:" + REQUESTBODY + ",BIZAO_TOKEN:" + BIZAO_TOKEN + ",BIZAO_ALIAS:" + BIZAO_ALIAS + " "

 

    return val

 


def getResponseData():
    DATETIME = str(datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3])
    TRANSACTION = "response"
    HTTP_STATUS = str(random.choice(HTTP_STATUS_LIST))
    RESPONSE_TIME = "616.0"

 

    val = " [" + DATETIME + "]" + "  INFO {REQUEST_RESPONSE_LOGGER} -  TRANSACTION:" + TRANSACTION + ",API_REQUEST_ID:" + API_REQUEST_ID + ",HTTP_STATUS:" + HTTP_STATUS + ",RESPONSE_TIME:" + RESPONSE_TIME + ",BODY:" + RESPONSEBOSY + " "
    return val

 


timer = int(mintt)
tpsSec = int(tps)
count = 0

 


def loopsecpart(length):
    while length != 0:
        f = open("/home/pradeep/Documents/ELK/logwriter/request-response-logger.log", "a")
        f.write(getRequestData() + "\n")
        f.write(getResponseData() + "\n")
        f.close()
        length = length - 1

 

    print("\n")

 


# t ps,lenth=tps
def looppersec(length):
    print('Starting ' + multiprocessing.current_process().name + ' - ' + str(datetime.datetime.now()))

 

    loopval1 = loopval
    while (length > 0):

 

        if (length < loopval1):
            loopval1 = length
            length = 0
        else:
            length = length - loopval1

 

        t = threading.Thread(target=loopsecpart, args=(loopval1,))
        t.start()
        t.join()
    global count
    print('Ending ' + multiprocessing.current_process().name + ' - ' + str(
        datetime.datetime.now()) + ' Record Count: ' + str(count))

 


startTime = str(datetime.datetime.now())
# time to run by seconds
while timer != 0:
    timer = timer - 1
    time.sleep(1)
    print(timer)
    multiprocessing.Process(target=looppersec, args=(tpsSec,)).start()

 

# END

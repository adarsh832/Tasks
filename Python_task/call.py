from twilio.rest import Client

client = Client(account_sid, acc_token)
call = client.calls.create(
    twiml='<Response><Say>Hi, this is a Python call</Say></Response>',
    to="+919837039028",
    from_="+14155238886"
)
import json
from django.http import HttpResponse

def ajax_error( etype='DefaultError', description='Internal server error', 
                additional_data={} ):
    
    msg =  {
        'reason': etype,
        'data': description
    }
    msg.update( additional_data )
    
    return HttpResponse( 
    
        json.dumps({
        
            'status' : 'fail',
            'msg': msg
        
        })
    
    )

def ajax_confirm( data={} ):

    return HttpResponse(

        json.dumps({
            
            'status' : 'ok',
            'msg': data
        
        })  
    )  

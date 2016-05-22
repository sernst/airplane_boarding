{{ settings.title }}
===================================

{{ settings.summary }}

 * __Trial ID__: {{ trial_id }}
 * __Passengers__: {{ passengers.shape[0] }}
 * __Time__: {{ status.time }}
 * __Population__: {{ settings.populate.type }}
    * _Group Count_: {{ settings.populate.groups }}
    * _Group Order_: {{ settings.populate.group_order }}
 * __Delay__:
    * _Seating_: {{ settings.delay.seating }}
    * _Interchange_: {{ settings.delay.interchange }}

import React from 'react';


const Message = ({alertType, message}) => {
    return (
            <li className={"alert " + alertType + " alert-dismissable list-group-item"}>
                <a href="#" className="close" data-dismiss="alert" aria-label="close">&times;</a>
                {message}
            </li>
    )
};

const MessageList = ({messages}) => {
    /*
    * Container holding all messages to the user.
    * messages should container list of tuples [(alertType, message), ...]
    * where alertType is the bootstrap class. ie. 'alert-success', 'alert-info', etc.
    * */
    return (
        <div className="row">
            <div className="col-sm-12">
                <ul className="list-group">
                    {messages.map((message, i) => {return <Message key={i} message={message['message']} alertType={message['alertType']}/>})}
                </ul>
            </div>
        </div>
    )
};

export default MessageList;
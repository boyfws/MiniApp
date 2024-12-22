// Css
import './FacCatCell.css'

// Ext lib
import {Cell, Switch} from "@telegram-apps/telegram-ui";
import React, {useEffect, useState} from "react";

// TODO: Сделать это гавно рабочим


const FavCatCell = ({cat_name}) => {
    const [clicked, setClicked] = useState(false);

    useEffect(() => {
        console.log(clicked);
    }, [clicked])

    return (
        <Cell className={"FavCatCell"}
              after={<Switch defaultChecked={clicked}/>}
        >
            {cat_name}
        </Cell>
    );
};

export default FavCatCell;
// Css
import './SearchFormAddress.css'


// Ext lib
import React, { useEffect, useState, useRef } from "react";

// Utils
import GetHandleSearchChange from "../../../utils/GetHadleSearchChange";
import {Input} from "@telegram-apps/telegram-ui";


const CALLBACK_DELAY_MS = 150;
const CALLBACK_SYMBOL_LIMIT = 2;


const SearchFormAddress = ({ChangeValueInUpperComp}) => {
    const [SearchValue, setSearchValue] = useState('');
    const debounceTimeout = useRef(null);

    const handleSearchChange = GetHandleSearchChange(
        debounceTimeout,
        setSearchValue,
        ChangeValueInUpperComp,
        CALLBACK_SYMBOL_LIMIT,
        CALLBACK_DELAY_MS
    )

    // Очистка таймера при размонтировании компонента
    useEffect(() => {
        return () => {
            if (debounceTimeout.current) {
                clearTimeout(debounceTimeout.current);
            }
        };
    }, []);


    return (
        <div className="SearchFormAddressWrapper">
            <Input status="focused"
               placeholder="Добавить новый ресторан"
               value={SearchValue}
               onChange={handleSearchChange}
               className={'input_for_address'}
            />
        </div>
    );
}

export default SearchFormAddress;
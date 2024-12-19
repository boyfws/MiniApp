// Css
import './SearchForm.css';

// Ext lib
import { Button, Input } from '@telegram-apps/telegram-ui';
import { Icon24Close } from '@telegram-apps/telegram-ui/dist/icons/24/close';
import React, { useState, useEffect, useRef } from 'react';

// State
import RestStore from "../../../state_management/stores/RestStore";

// Handlers
import GetHandleBackFromSearch from './utils/handleBackFromSearch';

// Utils
import GetHandleSearchChange from "../../../utils/GetHadleSearchChange";


const CALLBACK_DELAY_MS = 300;
const CALLBACK_SYMBOL_LIMIT = 2;


const SearchForm = ({setSearchClicked, ChangeValueInMainPage }) => {
    const [SearchValue, setSearchValue] = useState('');
    const debounceTimeout = useRef(null);
    const { setRestaurants, defaultRestaurants } = RestStore()


    const handleSearchChange = GetHandleSearchChange(
        debounceTimeout,
        setSearchValue,
        ChangeValueInMainPage,
        CALLBACK_SYMBOL_LIMIT,
        CALLBACK_DELAY_MS
    );

    // Очистка таймера при размонтировании компонента
    useEffect(() => {
        return () => {
            if (debounceTimeout.current) {
                clearTimeout(debounceTimeout.current);
            }
        };
    }, []);

    const handleBack = GetHandleBackFromSearch(setSearchClicked, setRestaurants, defaultRestaurants)

    return (
        <div className='InputWrapper'>
            <Input
                status="focused"
                placeholder="Write and clean me"
                value={SearchValue}
                onChange={handleSearchChange}
                after={
                    <Button
                        mode='filled'
                        size="s"
                        style={{ display: 'flex' }}
                        onClick={() => { handleBack(); setSearchValue(''); ChangeValueInMainPage(''); }}
                        className='close-icon'>
                        <Icon24Close className='icon' />
                    </Button>
                }
                className='input'
            />
        </div>
    );
}

export default SearchForm;
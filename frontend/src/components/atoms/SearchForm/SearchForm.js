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


const CALLBACK_DELAY_MS = 300;
const CALLBACK_SYMBOL_LIMIT = 2;


const SearchForm = ({setSearchClicked, ChangeValueInMainPage }) => {
    const [SearchValue, setSearchValue] = useState('');
    const debounceTimeout = useRef(null);
    const { setRestaurants, defaultRestaurants } = RestStore()


    const handleSearchChange = (event) => {
        const searchValue = event.target.value;
        setSearchValue(searchValue);

        // Очищаем предыдущий таймер
        if (debounceTimeout.current) {
            clearTimeout(debounceTimeout.current);
        }

        // Устанавливаем новый таймер
        debounceTimeout.current = setTimeout(() => {
            if (searchValue.length > CALLBACK_SYMBOL_LIMIT) {
                ChangeValueInMainPage(searchValue);
            }
        }, CALLBACK_DELAY_MS); // Задержка 
    };

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
        <div style={{ backgroundColor: 'var(--tgui--bg_color)', width: '100%' }}>
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
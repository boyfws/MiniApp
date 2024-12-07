// Css
import './UpperLevelInHeaderMainPage.css'

// Ext lib
import React, { useState, useEffect, useContext } from "react";

// State
import DefAddressStore from "../../../state_management/stores/DefAddressStore";
import RestStore from "../../../state_management/stores/RestStore";

// Handlers
import GetLoadRestFromSearch from './utils/GetNewRestFromSearch';

// Comp
import SearchForm from '../../atoms/SearchForm/SearchForm';
import AddressButton from '../../atoms/AddressButton/AdressButton';
import SearchButton from '../../atoms/SearchButton/SearchButton';
import ProfileAvatar from '../../atoms/ProfileAvatar/ProfileAvatar';


const UpperLevelInHeaderMainPage = ({setScrollPositionY, setModalState}) => {
    const [searchClicked, setSearchClicked] = useState(false);
    const [InputValue, setInputValue] = useState('');
    const { DefAddress } = DefAddressStore();
    const { setRestaurants } = RestStore();

    const LoadRestFromSearch = GetLoadRestFromSearch(
        DefAddress,
        InputValue, 
        setRestaurants
      );

    useEffect(LoadRestFromSearch, [InputValue]);

    return (

        <div className="upper-level-wrapper">

            <div className={`upper-level${searchClicked ? '-hidden' : ''}`}>

                <ProfileAvatar
                    setScrollPositionY={setScrollPositionY}
                    className='profile-avatar'
                />

                <AddressButton
                    className='adress-button'
                    onClick={() => {setModalState(true)}}
                />

                <SearchButton 
                    setSearchClicked={setSearchClicked} 
                    className='search-button' 
                />

            </div>

            <div className={`search${searchClicked ? '' : '-hidden'}`}>

                <SearchForm 
                    setSearchClicked={setSearchClicked}
                    ChangeValueInMainPage={setInputValue}
                />

            </div>

      </div>
    )
}


export default UpperLevelInHeaderMainPage
import './UpperLevelMainPage.css'

import SearchForm from '../../molecules/SearchForm/SearchForm';
import AddressButton from '../../atoms/AddressButton/AdressButton';
import SearchButton from '../../atoms/SearchButton/SearchButton';
import ProfileAvatar from '../../atoms/ProfileAvatar/ProfileAvatar';

import GetLoadRestFromSearch from '../../../webhooks/GetNewRestFromSearch';

import DefAddressStore from "../../../stores/DefAddressStore";
import RestStore from "../../../stores/RestStore";

import React, { useState, useEffect, useContext } from "react";
import { useHistory } from "react-router-dom";


const UpperLevelMainPage = ({setScrollPositionY, setModalState}) => {
    const [searchClicked, setSearchClicked] = useState(false);
    const [InputValue, setInputValue] = useState('');

    const history = useHistory();

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
                    history={history}
                    className='profile-avatar'
                />

                <AddressButton
                    defaultAdress={DefAddress}
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
                    ChangeValueInMainPage={setInputValue}/>
            </div>

      </div>
    )
}


export default UpperLevelMainPage
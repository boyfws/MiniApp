// Css
import './RestaurantPage.css'

// Ext lib
import React, {useEffect, useState} from 'react';
import { useHistory, useParams } from 'react-router-dom';

// Comp
import LoaderWrapperRestPage from "../../components/templates/LoaderWrapperRestPage/LoaderWrapperRestPage";
import RestPageTemp from "../../components/templates/RestPageTemp/RestPageTemp";

// Utils
import GetLoadRestData from "./utils/LoadRestData";
import GetHandleGoBack from "./utils/handleGoBack";
import GetLoadMenu from "./utils/LoadMenu";
import {Subheadline} from "@telegram-apps/telegram-ui";
import PreapareGeoJsonForDisplay from "../../components/atoms/RestAddressTitle/utils/PrepareGeoJsonForDisplay";


const RestaurantPage = () => {
  const history = useHistory();
  const id = useParams().id;

  const [RestData, SetRestData] = useState({});
  const [Menu, setMenu] = useState({});

  const [RestDataLoading, setRestDataLoading] = useState(true);
  const [MenuLoading, setMenuLoading] = useState(true);


  const [showContent, setShowContent] = useState(false);

  
  const LoadRestData = GetLoadRestData(
      setRestDataLoading,
      id,
      SetRestData
  );

  const LoadMenu = GetLoadMenu(
      setMenuLoading,
      id,
      setMenu);

  const handleGoBack = GetHandleGoBack(history);



  useEffect(() => {
      window.Telegram.WebApp.BackButton.onClick(handleGoBack);
      window.Telegram.WebApp.BackButton.show()
  }, [])


  useEffect(LoadRestData, [])

  useEffect(LoadMenu, [])


  if (!showContent) {
    return (
        <LoaderWrapperRestPage
            RestDataLoading={RestDataLoading}
            MenuLoading={MenuLoading}
            setShowContent={setShowContent}
        />
    )
  }

  return (
    <div className="RestaurantPage">
      <Title>
        {RestData.name}
      </Title>
      <Subheadline>
        {PreapareGeoJsonForDisplay(RestData.address)}
      </Subheadline>
      <div className="photos">
        Тут типа будут фотки (сори решили сделать хоть как то, так как красиво не успели)
      </div>


    </div>
  );
};

export default RestaurantPage;

// Ext lib
import React, { useContext } from "react";
import { Divider } from "@telegram-apps/telegram-ui";

// State
import { CategoriesContext } from "../../../state_management/context/Contexts/CategoriesContext";

// Comp
import FavCatCell from "../../atoms/FavCatCell/FavCatCell";

const ListOfManCat = ({}) => {
    const {categories} = useContext(CategoriesContext);
    return (
        <div>
            {categories.map((category, index) => (
                <React.Fragment key={index}>
                    <FavCatCell
                        category={category}
                    />
                    {index < categories.length - 1 && <Divider/>}
                </React.Fragment>
            ))}
        </div>
    );
};

export default ListOfManCat;
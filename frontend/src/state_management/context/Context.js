import { MainPageLoadingContextProvider } from "./Contexts/MainPageLoadingContext";
import { CategoriesContextProvider } from "./Contexts/CategoriesContext";


const ContextProvider = ({ children }) => {
    return (
        <MainPageLoadingContextProvider>
                <CategoriesContextProvider>
                    {children}
                </CategoriesContextProvider>
        </MainPageLoadingContextProvider>
    );
};

export {ContextProvider};
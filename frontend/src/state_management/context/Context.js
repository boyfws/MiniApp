import { LoadingContextProvider } from "./Contexts/LoadingContext";
import { CategoriesContextProvider } from "./Contexts/CategoriesContext";


const ContextProvider = ({ children }) => {
    return (
        <LoadingContextProvider>
                <CategoriesContextProvider>
                    {children}
                </CategoriesContextProvider>
        </LoadingContextProvider>
    );
};

export {ContextProvider};
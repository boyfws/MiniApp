import { DefAddressProvider } from "./Contexts/DefAddressContext";
import { LoadingContextProvider } from "./Contexts/LoadingContext";

const ContextProvider = ({ children }) => {
    return (
        <LoadingContextProvider>
            <DefAddressProvider>
                {children}
            </DefAddressProvider>
        </LoadingContextProvider>
    );
};

export {ContextProvider};
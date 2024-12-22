import { create } from 'zustand'


const AddressesStore =
    // TODO: Добавть хендл ситуации с дублированием адресов
    create(set => (
            {Addresses: [],
            SetAddresses: addresses => set({ Addresses: addresses }),
            addAddress: (address) =>
                set((state) => {
                    if (!state.Addresses.some(item => item.properties === address.properties)) {
                        return {
                            Addresses: [...state.Addresses, address],
                        };
                    }
                    return state;
                }),

            removeAddress: (address) =>
                set((state) => ({
                    Addresses: state.Addresses.filter((item) => item !== address),
                })),
            }
        )
    )


export default AddressesStore
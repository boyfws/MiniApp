import { create } from 'zustand'


const AddressesStore =
    create(set => (
            {Addresses: [],
            SetAddresses: addresses => set({ Addresses: addresses }),
            addAddress: (address) =>
                set((state) => ({
                    Addresses: [...state.Addresses, address],
                })),

            removeAddress: (address) =>
                set((state) => ({
                    Addresses: state.Addresses.filter((item) => item !== address),
                })),
            }
        )
    )


export default AddressesStore
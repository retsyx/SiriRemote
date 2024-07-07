#!/usr/bin/env python

# Copyright 2024.
# This file is part of SiriRemote.
# SiriRemote is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

import subprocess

from bluepy3 import btle
from bluepy3.btle import AssignedNumbers

class Scanner(object):
    def __init__(self):
        self.scanner = btle.Scanner()
        self.scanner.withDelegate(self)
        self.pairing = False

    def handleDiscovery(self, entry, isNewDev, isNewData):
        pass

    def check_pair(self, entry):
        manufacturer = entry.getValueText(255)

        if manufacturer is None:
            return

        # First 2 bytes are manufacturer ID 004C which is Apple
        # Last 2 bytes are the PNP product ID:
        # Gen 1 - 0266
        # Gen 1.5 - 026D
        # Gen 2 - 0314
        # Gen 3 - 0315
        if (not manufacturer.startswith('4c008a076602') # gen 1
            and not manufacturer.startswith('4c008a076d02') # gen 1.5
            and not manufacturer.startswith('4c00070d021403') # gen 2
            and not manufacturer.startswith('4c00070d021503') # gen 3
            ):
            return

        if entry.rssi < -50:
            print('Bring the remote closer to me!\n')
            return

        try:
            device = btle.Peripheral(entry)
        except btle.BTLEException as e:
            return

        print('Pairing...')
        try:
            self.pairing = True
            device.setBondable(True)
            device.setSecurityLevel(btle.SEC_LEVEL_MEDIUM)
            public_addr, _ = device.pair()
            self.pairing = False
            print('Paired!')

            device.getServices()
            device_info_svc = device.getServiceByUUID(AssignedNumbers.device_information)
            serial_number = None
            for ch in device_info_svc.getCharacteristics():
                if ch.uuid == AssignedNumbers.serial_number_string:
                    serial_number = device.readCharacteristic(ch.getHandle()).decode()
                    break

            return serial_number, public_addr
        except btle.BTLEManagementError:
            print("Pairing failed. Try resetting the remote by pressing 'HOME' and '-' for"\
                  "a few seconds.")
            print('Trying again!\n')

    def scan(self):
        while True:
            try:
                entries = self.scanner.scan(1)
                for entry in entries:
                    remote = self.check_pair(entry)
                    if remote is not None:
                        return remote
            except (btle.BTLEConnectError, BrokenPipeError) as e:
                if self.pairing:
                    print('Pairing failed. Try resetting the remote.')
                    print('Trying again!\n')

def main():
    print("Bring the remote close to me, and press 'MENU' and '+' on the remote for a few seconds.\n")

    scanner = Scanner()
    serial_number, public_addr = scanner.scan()

    print(f'Paired with remote!')
    print(f'Serial number: {serial_number}')
    print(f'MAC address: {public_addr}')

    # The bluetooth subsystem likes to exclusively connect to remotes immediately after pairing,
    # thus preventing us from using the remote. So use bluetoothctl to disconnect from the remote.
    subprocess.run(['/usr/bin/bluetoothctl', 'disconnect', public_addr], capture_output=True)

if __name__ == '__main__':
    main()

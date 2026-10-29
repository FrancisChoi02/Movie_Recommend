### Real World Back-end Coding Exercise - Device Fleet - 30-min Variant

**Topic**: Device Status Transition Validation

**Language**: Python

**Prompt**:

We are building Device Fleet, a back-end system that manages the lifecycle of IoT devices across multiple locations.

**Definitions**:

- A "device" is an object representing a single piece of IoT hardware deployed at a location. A device has:
    - `device_id`
    - `device_type`
    - `location`
    - `status`
    - `registered_day` (the day number, relative to a fixed reference point, on which the device was registered into the fleet)
    - `next_maintenance_day` (the day number by which the device's next scheduled maintenance must occur)
    - `failure_count` (the running count of failures reported by the device since registration)
- A device's status can be one of:
    - REGISTERED
    - ACTIVE
    - SUSPENDED
    - MAINTENANCE_DUE
    - RETIRED

The `DeviceLifecycleManager` class manages devices.

**Tasks**:

1. Read through and understand the code below, feel free to run it.
2. The test for `DeviceLifecycleManager` is not passing due to a bug in the code. Make the necessary changes to `DeviceLifecycleManager` to fix the bug.

---

**Provided Code**:

```
import unittest

class Device:
    def __init__(
        self,
        device_id,
        device_type,
        location,
        status,
        registered_day,
        next_maintenance_day,
        failure_count,
    ):
        """Represents a single device with its identifying and lifecycle attributes."""
        self.device_id = device_id
        self.device_type = device_type
        self.location = location
        self.status = status
        self.registered_day = registered_day
        self.next_maintenance_day = next_maintenance_day
        self.failure_count = failure_count

class DeviceLifecycleConfig:
    SUPPORTED_DEVICE_TYPES = {
        "SENSOR",
        "CAMERA",
        "ACTUATOR"
    }

    VALID_STATUSES = {
        "REGISTERED",
        "ACTIVE",
        "SUSPENDED",
        "MAINTENANCE_DUE",
        "RETIRED"
    }

    VALID_TRANSITIONS = {
        "REGISTERED": {"ACTIVE", "RETIRED"},
        "ACTIVE": {"SUSPENDED", "MAINTENANCE_DUE", "RETIRED"},
        "SUSPENDED": {"ACTIVE", "RETIRED"},
        "MAINTENANCE_DUE": {"ACTIVE", "RETIRED"},
        "RETIRED": set()
    }

class DeviceLifecycleManager:
    def __init__(self):
        """Manages the collection of registered devices, keyed by device ID."""
        self.devices = {}

    def update_device_status(self, device_id, new_status):
        """Updates the device's status if the transition is valid, and returns whether the update was applied."""
        device = self.devices.get(device_id)

        if device is None:
            return False

        if new_status not in DeviceLifecycleConfig.VALID_STATUSES:
            return False

        device.status = new_status
        return True

class TestSuite(unittest.TestCase):
    def test_update_device_status(self):
        """Test update device status."""
        # ACTIVE -> SUSPENDED: valid transition.
        manager_a = DeviceLifecycleManager()
        manager_a.devices["D-1"] = Device(
            "D-1", "SENSOR", "WAREHOUSE_A", "ACTIVE", 10, 50, 1
        )
        result_a = manager_a.update_device_status("D-1", "SUSPENDED")
        self.assertTrue(result_a)
        self.assertEqual("SUSPENDED", manager_a.devices["D-1"].status)

        # MAINTENANCE_DUE -> ACTIVE.
        manager_b = DeviceLifecycleManager()
        manager_b.devices["D-3"] = Device(
            "D-3", "ACTUATOR", "WAREHOUSE_B", "MAINTENANCE_DUE", 1, 15, 2
        )
        result_b = manager_b.update_device_status("D-3", "ACTIVE")
        self.assertTrue(result_b)
        self.assertEqual("ACTIVE", manager_b.devices["D-3"].status)

        # REGISTERED -> RETIRED.
        manager_c = DeviceLifecycleManager()
        manager_c.devices["D-4"] = Device(
            "D-4", "SENSOR", "WAREHOUSE_C", "REGISTERED", 3, 30, 0
        )
        result_c = manager_c.update_device_status("D-4", "RETIRED")
        self.assertTrue(result_c)
        self.assertEqual("RETIRED", manager_c.devices["D-4"].status)

        # SUSPENDED -> ACTIVE.
        manager_d = DeviceLifecycleManager()
        manager_d.devices["D-5"] = Device(
            "D-5", "CAMERA", "WAREHOUSE_A", "SUSPENDED", 7, 40, 1
        )
        result_d = manager_d.update_device_status("D-5", "ACTIVE")
        self.assertTrue(result_d)
        self.assertEqual("ACTIVE", manager_d.devices["D-5"].status)

    def test_update_device_status_2(self):
        """Test update device status."""
        # ACTIVE -> RETIRED: invalid transition.
        manager_a = DeviceLifecycleManager()
        manager_a.devices["D-1"] = Device(
            "D-1", "SENSOR", "WAREHOUSE_A", "ACTIVE", 10, 50, 1
        )
        result_a = manager_a.update_device_status("D-1", "RETIRED")
        self.assertFalse(result_a)
        self.assertEqual("ACTIVE", manager_a.devices["D-1"].status)

        # RETIRED device.
        manager_b = DeviceLifecycleManager()
        manager_b.devices["D-2"] = Device(
            "D-2", "CAMERA", "WAREHOUSE_A", "RETIRED", 5, 20, 4
        )
        result_b = manager_b.update_device_status("D-2", "ACTIVE")
        self.assertFalse(result_b)
        self.assertEqual("RETIRED", manager_b.devices["D-2"].status)

        # Same-status transition.
        manager_c = DeviceLifecycleManager()
        manager_c.devices["D-1"] = Device(
            "D-1", "SENSOR", "WAREHOUSE_A", "ACTIVE", 10, 50, 1
        )
        result_c = manager_c.update_device_status("D-1", "ACTIVE")
        self.assertFalse(result_c)
        self.assertEqual("ACTIVE", manager_c.devices["D-1"].status)

    def test_update_device_status_3(self):
        """Test update device status."""
        # Unknown device ID.
        manager_a = DeviceLifecycleManager()
        result_a = manager_a.update_device_status("UNKNOWN", "ACTIVE")
        self.assertFalse(result_a)

        # Unrecognized status.
        manager_b = DeviceLifecycleManager()
        manager_b.devices["D-1"] = Device(
            "D-1", "SENSOR", "WAREHOUSE_A", "ACTIVE", 10, 50, 1
        )
        result_b = manager_b.update_device_status("D-1", "BROKEN")
        self.assertFalse(result_b)
        self.assertEqual("ACTIVE", manager_b.devices["D-1"].status)

if __name__ == "__main__":
    unittest.main()
```

---

**Clarifications**:

- Devices move between registered, active, suspended, maintenance due, and retired states, and only certain transitions between those states are allowed.
- A transition from a status back to that same status is never considered valid, even though the status itself is recognized.
- Once a device becomes retired, it can no longer move to any other status.
- If the device does not exist, or the requested status is not one of the recognized statuses, no update should happen.
- When the transition is invalid for any reason, the device's existing status must remain unchanged.

**Pitfalls**:

- Validating the new status in isolation, without checking whether it's actually reachable from the device's current status.
- Assuming any two recognized statuses can be transitioned between as long as both are valid values, rather than checking against the specific set of allowed transitions.
- Updating the device's status before confirming the transition is valid.
- Raising an exception instead of returning a plain failure indicator when a transition is invalid.

**Python Solution Skeleton**:

```
def update_device_status(self, device_id, new_status):
    device = self.devices.get(device_id)

    if device is None:
        return False

    if new_status not in DeviceLifecycleConfig.VALID_STATUSES:
        return False

    allowed_statuses = DeviceLifecycleConfig.VALID_TRANSITIONS.get(
        device.status,
        set()
    )

    if new_status not in allowed_statuses:
        return False

    device.status = new_status
    return True
```

### Coding Question: Device Registration and Active Device Counts

**Prompt**

We are extending Device fleet to register new devices and track how many are active by type. This helps operations and procurement teams see what's actually deployed and plan capacity.

Add two functions to the `DeviceLifecycleManager` class:

**2-1) add_device**

The `add_device` function takes a device object. It should add the device only when all of the following conditions are satisfied:

- Its device ID is not already used by another device.
- Its status is valid.
- Its device type is supported.
- Its registration day is zero or greater.

Return true when the device is added and false when any validation condition is not satisfied.

The function must leave the existing device collection unchanged when the device is invalid.

**2-2) get_active_device_counts_by_type**

The `get_active_device_counts_by_type` function takes no arguments. It should return a dictionary mapping each device type to the number of active devices of that type.

Device types with zero active devices should not be present in the dictionary.

---

**Test Code**

```
def test_add_device_1(self):
    """Test that a valid device is added and stored, and a duplicate device ID is rejected."""
    manager = DeviceLifecycleManager()

    # A valid device is added and stored by its device ID.
    first = Device(
        "D-1", "SENSOR", "WAREHOUSE_A", "REGISTERED", 10, 40, 0
    )
    self.assertTrue(manager.add_device(first))
    self.assertIn("D-1", manager.devices)

    # Duplicate device ID.
    second = Device(
        "D-1", "CAMERA", "WAREHOUSE_B", "ACTIVE", 20, 50, 1
    )
    self.assertFalse(manager.add_device(second))
    self.assertEqual(first, manager.devices["D-1"])

def test_add_device_2(self):
    """Test that a device failing any single validation rule is rejected and the collection is left unchanged."""
    manager = DeviceLifecycleManager()

    # Unsupported device type is rejected and never stored.
    unsupported_type = Device(
        "D-1", "THERMOSTAT", "WAREHOUSE_A", "REGISTERED", 10, 40, 0
    )
    self.assertFalse(manager.add_device(unsupported_type))
    self.assertNotIn("D-1", manager.devices)

    # Invalid status is rejected.
    invalid_status = Device(
        "D-1", "SENSOR", "WAREHOUSE_A", "BROKEN", 10, 40, 0
    )
    self.assertFalse(manager.add_device(invalid_status))
    self.assertNotIn("D-1", manager.devices)

    # Negative registered day is rejected.
    negative_registered_day = Device(
        "D-1", "SENSOR", "WAREHOUSE_A", "REGISTERED", -1, 40, 0
    )
    self.assertFalse(manager.add_device(negative_registered_day))
    self.assertNotIn("D-1", manager.devices)

def test_add_device_3(self):
    """Test that a registered day of 0 is a valid boundary value."""
    manager = DeviceLifecycleManager()

    # Registered day of 0.
    zero_registered_day = Device(
        "D-1", "SENSOR", "WAREHOUSE_A", "REGISTERED", 0, 10, 0
    )
    self.assertTrue(manager.add_device(zero_registered_day))

def test_get_active_device_counts_by_type_1(self):
    """Test that active devices are counted and grouped by device type, ignoring non-active devices."""
    manager = DeviceLifecycleManager()
    devices = [
        Device("D-1", "SENSOR", "WAREHOUSE_A", "ACTIVE", 10, 40, 0),
        Device("D-2", "SENSOR", "WAREHOUSE_B", "ACTIVE", 12, 42, 1),
        Device("D-3", "CAMERA", "WAREHOUSE_A", "SUSPENDED", 15, 45, 2),
        Device("D-4", "GATEWAY", "WAREHOUSE_C", "ACTIVE", 20, 50, 0),
        # REGISTERED device.
        Device("D-5", "CAMERA", "WAREHOUSE_B", "REGISTERED", 30, 60, 0)
    ]

    for device in devices:
        manager.devices[device.device_id] = device

    result = manager.get_active_device_counts_by_type()

    self.assertEqual({"SENSOR": 2, "GATEWAY": 1}, result)

def test_get_active_device_counts_by_type_2(self):
    """Test that a device type with no active devices does not appear in the result."""
    manager = DeviceLifecycleManager()
    manager.devices["D-1"] = Device(
        "D-1", "SENSOR", "WAREHOUSE_A", "SUSPENDED", 10, 40, 0
    )

    result = manager.get_active_device_counts_by_type()

    self.assertEqual({}, result)
```

---

**Clarifications**

No additional clarifications are required.

**Pitfalls**

- Replacing an existing device when a new device is added with the same ID.
- Storing the device before all validation checks are complete.
- Hardcoding supported device types or valid statuses instead of using `DeviceLifecycleConfig`.
- Including device types with zero active devices in the result.

---

**Python Solution Skeleton**

```
def add_device(self, device):
    if device.device_id in self.devices:
        return False

    if device.device_type not in DeviceLifecycleConfig.SUPPORTED_DEVICE_TYPES:
        return False

    if device.status not in DeviceLifecycleConfig.VALID_STATUSES:
        return False

    if device.registered_day < 0:
        return False

    self.devices[device.device_id] = device
    return True

def get_active_device_counts_by_type(self):
    counts = {}

    for device in self.devices.values():
        if device.status != "ACTIVE":
            continue

        counts[device.device_type] = counts.get(device.device_type, 0) + 1

    return counts
```

### **Topic**: Marking Devices Due for Maintenance

**Prompt**:

```
We now need to flag devices that are due for maintenance. This lets maintenance teams know which devices need a technician dispatched before they keep running past their scheduled service window.

Add one function to the DeviceLifecycleManager class.

3-1) mark_devices_due_for_maintenance

The mark_devices_due_for_maintenance function takes a current day and a maximum failure count. It should update every qualifying device's status to MAINTENANCE_DUE, following these rules:
- A device qualifies only if its status is ACTIVE, its maintenance day is on or before the given current day, and its failure count is at or below the given maximum failure count.
- A device whose failure count is above the maximum is excluded, even if its maintenance day has arrived - it needs replacement rather than maintenance.
- Every other device is left unchanged, and no other attribute of a qualifying device is modified.

Return the number of devices whose status changed.

If the current day is negative, or the maximum failure count is negative, return 0 and make no changes.
```

**Test Cases**:

```
def test_mark_devices_due_for_maintenance_1(self):
    """Test that ACTIVE devices due for maintenance are marked and counted, covering the inclusive day boundary, the failure count boundary, multiple qualifying devices, and preservation of other attributes."""
    # Device due exactly on the current day (boundary); another not yet due.
    manager = DeviceLifecycleManager()
    manager.devices["D-1"] = Device(
        "D-1", "SENSOR", "WAREHOUSE_A", "ACTIVE", 10, 30, 0
    )
    manager.devices["D-2"] = Device(
        "D-2", "CAMERA", "WAREHOUSE_A", "ACTIVE", 10, 40, 1
    )

    updated = manager.mark_devices_due_for_maintenance(30, 5)

    self.assertEqual(1, updated)
    self.assertEqual("MAINTENANCE_DUE", manager.devices["D-1"].status)
    self.assertEqual("ACTIVE", manager.devices["D-2"].status)

    # Multiple ACTIVE devices due on the current day.
    manager_multi = DeviceLifecycleManager()
    manager_multi.devices["D-1"] = Device(
        "D-1", "SENSOR", "WAREHOUSE_A", "ACTIVE", 10, 30, 0
    )
    manager_multi.devices["D-2"] = Device(
        "D-2", "CAMERA", "WAREHOUSE_A", "ACTIVE", 10, 40, 1
    )

    updated_multi = manager_multi.mark_devices_due_for_maintenance(40, 5)

    self.assertEqual(2, updated_multi)
    self.assertEqual("MAINTENANCE_DUE", manager_multi.devices["D-1"].status)
    self.assertEqual("MAINTENANCE_DUE", manager_multi.devices["D-2"].status)

    # Other device attributes on a marked device.
    manager_attrs = DeviceLifecycleManager()
    manager_attrs.devices["D-1"] = Device(
        "D-1", "SENSOR", "WAREHOUSE_A", "ACTIVE", 10, 30, 0
    )

    device = manager_attrs.devices["D-1"]
    original_maintenance_day = device.next_maintenance_day
    original_failures = device.failure_count

    updated_attrs = manager_attrs.mark_devices_due_for_maintenance(30, 5)

    self.assertEqual(1, updated_attrs)
    self.assertEqual(original_maintenance_day, device.next_maintenance_day)
    self.assertEqual(original_failures, device.failure_count)

    # Failure count exactly equal to max failure count (boundary).
    manager_failure_boundary = DeviceLifecycleManager()
    manager_failure_boundary.devices["D-1"] = Device(
        "D-1", "SENSOR", "WAREHOUSE_A", "ACTIVE", 10, 30, 5
    )

    updated_failure_boundary = manager_failure_boundary.mark_devices_due_for_maintenance(30, 5)

    self.assertEqual(1, updated_failure_boundary)
    self.assertEqual("MAINTENANCE_DUE", manager_failure_boundary.devices["D-1"].status)

def test_mark_devices_due_for_maintenance_2(self):
    """Test that devices which are not ACTIVE (suspended, retired, or already awaiting maintenance), or whose failure count exceeds the maximum, are never changed or counted."""
    manager = DeviceLifecycleManager()
    manager.devices["D-3"] = Device(
        "D-3", "SENSOR", "WAREHOUSE_B", "SUSPENDED", 10, 20, 2
    )
    # Device already MAINTENANCE_DUE.
    manager.devices["D-4"] = Device(
        "D-4", "SENSOR", "WAREHOUSE_C", "MAINTENANCE_DUE", 10, 15, 3
    )
    # RETIRED device.
    manager.devices["D-5"] = Device(
        "D-5", "CAMERA", "WAREHOUSE_C", "RETIRED", 5, 10, 5
    )

    updated = manager.mark_devices_due_for_maintenance(100, 100)

    self.assertEqual(0, updated)
    self.assertEqual("SUSPENDED", manager.devices["D-3"].status)
    self.assertEqual("MAINTENANCE_DUE", manager.devices["D-4"].status)
    self.assertEqual("RETIRED", manager.devices["D-5"].status)

    # Failure count above max failure count, despite being ACTIVE and due.
    manager_failures = DeviceLifecycleManager()
    manager_failures.devices["D-6"] = Device(
        "D-6", "SENSOR", "WAREHOUSE_A", "ACTIVE", 10, 30, 6
    )

    updated_failures = manager_failures.mark_devices_due_for_maintenance(30, 5)

    self.assertEqual(0, updated_failures)
    self.assertEqual("ACTIVE", manager_failures.devices["D-6"].status)

def test_mark_devices_due_for_maintenance_3(self):
    """Test the negative current_day guard, the negative max_failure_count guard, the current_day=0 boundary, and an empty device collection."""
    # Negative current_day devices.
    manager = DeviceLifecycleManager()
    manager.devices["D-1"] = Device(
        "D-1", "SENSOR", "WAREHOUSE_A", "ACTIVE", 10, 30, 0
    )
    manager.devices["D-2"] = Device(
        "D-2", "CAMERA", "WAREHOUSE_A", "ACTIVE", 10, 40, 1
    )

    updated = manager.mark_devices_due_for_maintenance(1, 5)

    self.assertEqual(0, updated)
    self.assertEqual("ACTIVE", manager.devices["D-1"].status)
    self.assertEqual("ACTIVE", manager.devices["D-2"].status)

    # Device with a negative next maintenance day.
    negative_day_manager = DeviceLifecycleManager()
    negative_day_manager.devices["D-7"] = Device(
        "D-7", "SENSOR", "WAREHOUSE_A", "ACTIVE", 10, -5, 0
    )

    negative_day_updated = negative_day_manager.mark_devices_due_for_maintenance(1, 5)

    self.assertEqual(0, negative_day_updated)
    self.assertEqual("ACTIVE", negative_day_manager.devices["D-7"].status)

    # Negative max failure count.
    negative_max_manager = DeviceLifecycleManager()
    negative_max_manager.devices["D-1"] = Device(
        "D-1", "SENSOR", "WAREHOUSE_A", "ACTIVE", 10, 30, 0
    )

    negative_max_updated = negative_max_manager.mark_devices_due_for_maintenance(30, 1)

    self.assertEqual(0, negative_max_updated)
    self.assertEqual("ACTIVE", negative_max_manager.devices["D-1"].status)

    # Device with a negative failure count, otherwise due.
    negative_failure_manager = DeviceLifecycleManager()
    negative_failure_manager.devices["D-8"] = Device(
        "D-8", "SENSOR", "WAREHOUSE_A", "ACTIVE", 10, 30, -2
    )

    negative_failure_updated = negative_failure_manager.mark_devices_due_for_maintenance(30, 1)

    self.assertEqual(0, negative_failure_updated)
    self.assertEqual("ACTIVE", negative_failure_manager.devices["D-8"].status)

    # Current day of 0 (boundary).
    zero_manager = DeviceLifecycleManager()
    zero_manager.devices["D-1"] = Device(
        "D-1", "SENSOR", "WAREHOUSE_A", "ACTIVE", 10, 0, 0
    )

    zero_updated = zero_manager.mark_devices_due_for_maintenance(0, 5)

    self.assertEqual(1, zero_updated)
    self.assertEqual("MAINTENANCE_DUE", zero_manager.devices["D-1"].status)

    # Empty device collection.
    empty_manager = DeviceLifecycleManager()

    empty_updated = empty_manager.mark_devices_due_for_maintenance(0, 5)

    self.assertEqual(0, empty_updated)
```

**Clarifications**:

No additional clarifications are required.

**Pitfalls**:

- Using a strict less-than comparison instead of an inclusive one, for either the day or the failure count boundary.
- Changing devices that are suspended, retired, or already awaiting maintenance.
- Modifying any other device attribute when updating status.
- Miscounting devices that qualify versus devices that actually changed.
- Not treating a negative current day, or a negative maximum failure count, as an early guard before other processing.
- Marking a device due for maintenance without also checking its failure count against the maximum.

**Python Solution Skeleton**:

```
def mark_devices_due_for_maintenance(self, current_day, max_failure_count):
    if current_day < 0:
        return 0

    if max_failure_count < 0:
        return 0

    updated_count = 0

    for device in self.devices.values():
        if (
            device.status == "ACTIVE"
            and device.next_maintenance_day <= current_day
            and device.failure_count <= max_failure_count
        ):
            device.status = "MAINTENANCE_DUE"
            updated_count += 1

    return updated_count
```
from collections import deque, OrderedDict

def simulate_LRU(pages, num_frames):
    frame_set = set()
    frame_list = deque()
    page_faults = 0
    page_fault_details = []

    for page in pages:
        if page not in frame_set:
            if len(frame_list) == num_frames:
                removed_page = frame_list.popleft()
                frame_set.remove(removed_page)
            frame_list.append(page)
            frame_set.add(page)
            page_faults += 1
            page_fault_details.append(f"Step {len(page_fault_details) + 1}: Page fault ({page}) - Page Table: {frame_set}, Frames: {list(frame_list)}, Faults: {page_faults}")
        else:
            frame_list.remove(page)
            frame_list.append(page)
            page_fault_details.append(f"Step {len(page_fault_details) + 1}: Page hit ({page}) - Page Table: {frame_set}, Frames: {list(frame_list)}, Faults: {page_faults}")

    return page_fault_details, page_faults

def simulate_FIFO(pages, num_frames):
    frame_list = deque()
    frame_set = set()
    page_faults = 0
    page_fault_details = []

    for page in pages:
        if page not in frame_set:
            if len(frame_list) == num_frames:
                removed_page = frame_list.popleft()
                frame_set.remove(removed_page)
            frame_list.append(page)
            frame_set.add(page)
            page_faults += 1
            page_fault_details.append(f"Step {len(page_fault_details) + 1}: Page fault ({page}) - Page Table: {frame_set}, Frames: {list(frame_list)}, Faults: {page_faults}")
        else:
            page_fault_details.append(f"Step {len(page_fault_details) + 1}: Page hit ({page}) - Page Table: {frame_set}, Frames: {list(frame_list)}, Faults: {page_faults}")

    return page_fault_details, page_faults

def simulate_optimal(pages, num_frames):
    frame_list = []
    page_faults = 0
    page_fault_details = []

    def predict_future_usage(pages, start_idx, frame_list):
        future_indices = {}
        for i in range(start_idx, len(pages)):
            page = pages[i]
            if page in frame_list:
                future_indices[page] = i
            if len(future_indices) == len(frame_list):
                break
        return future_indices

    for i, page in enumerate(pages):
        if page not in frame_list:
            if len(frame_list) < num_frames:
                frame_list.append(page)
            else:
                future_indices = predict_future_usage(pages, i + 1, frame_list)
                if future_indices:
                    page_to_replace = min(future_indices, key=future_indices.get)
                    frame_list[frame_list.index(page_to_replace)] = page
            page_faults += 1
            page_fault_details.append(f"Step {len(page_fault_details) + 1}: Page fault ({page}) - Page Table: {set(frame_list)}, Frames: {frame_list}, Faults: {page_faults}")
        else:
            page_fault_details.append(f"Step {len(page_fault_details) + 1}: Page hit ({page}) - Page Table: {set(frame_list)}, Frames: {frame_list}, Faults: {page_faults}")

    return page_fault_details, page_faults

def main():
    page_reference_string = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    num_frames = 4

    print("Page reference string:", page_reference_string)
    print("Number of frames:", num_frames)

    # Simulate LRU
    print("\nFor LRU Algorithm:")
    lru_details, lru_faults = simulate_LRU(page_reference_string, num_frames)
    for detail in lru_details:
        print(detail)
    print(f"Total Page Faults: {lru_faults}")

    # Simulate Optimal
    print("\nFor Optimal Algorithm:")
    optimal_details, optimal_faults = simulate_optimal(page_reference_string, num_frames)
    for detail in optimal_details:
        print(detail)
    print(f"Total Page Faults: {optimal_faults}")

    # Simulate FIFO
    print("\nFor FIFO Algorithm:")
    fifo_details, fifo_faults = simulate_FIFO(page_reference_string, num_frames)
    for detail in fifo_details:
        print(detail)
    print(f"Total Page Faults: {fifo_faults}")

if __name__ == "__main__":
    main()
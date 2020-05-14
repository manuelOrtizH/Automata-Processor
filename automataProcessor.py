#Command to install PrettyTable Library: pip3 install PrettyTable or pip install PrettyTable
from prettytable import PrettyTable
def get_transition(states, letter, transitions):
	result = {'Set_states': []}
	for state in states:
		if letter in transitions[state]:
			for each in transitions[state][letter]: 
				if each not in result['Set_states']: 
					result['Set_states'].append(each)
	return result['Set_states']

def to_dfa(new_set_states, d_ndfa,set_states): 
	key_name = ",".join(new_set_states)
	if key_name in set_states.keys(): 
		return set_states
	set_states[key_name] = {}
	for letter in d_ndfa['Alphabet']: 
		list_trans = get_transition(new_set_states, letter, d_ndfa['Transitions'])
		if len(list_trans) > 0: 
			set_states[key_name][letter] = list_trans
			to_dfa(list_trans, d_ndfa,set_states) 
	return set_states

def read_data():
	content = open("test1.txt","r").readlines()
	lines = [line.strip() for line in content]
	states = lines[0].split(",")
	alphabet = lines[1].split(",")
	initial_state = lines[2].split(",")
	final_states = lines[3].split(",")
	lines_trans = [line.replace("=>",",").split(",") for line in lines[4:]]
	d_ndfa = {'States': states, 'Alphabet': alphabet, 'Initial_state': initial_state, 'Final_states': final_states, 'Transitions': {}}
	for state in states:
		d_ndfa['Transitions'][state] = {} 
	for each in lines_trans:
		d_ndfa['Transitions'][each[0]][each[1]] = each[2:] 
	return d_ndfa

def print_set_states(set_states):
	print("\nTransition of Set of States\n".center(20))
	for sets in set_states:
		for transition in set_states[sets]:
			print(sets,",",transition, "=>", set_states[sets][transition], "\n")

def equivalence(set_states):
	i = 0
	d_dfa={}
	d_eq={}
	for sets in set_states:
		d_eq[sets] = "q"+str(i) 
		d_dfa['q'+str(i)] = set_states[sets] 
		i+=1
	for key in d_dfa: 
		for letter, trans in d_dfa[key].items():
			key_name = ",".join(trans)
			if key_name in d_eq.keys(): 
				d_dfa[key][letter] = d_eq[key_name] 
	return d_dfa

def print_table(set_states, alphabet):
	print("Dfa transition table\n".center(25))
	table = PrettyTable()
	header = ['States']+alphabet
	table.field_names = header
	for s in set_states:
		row_data = []
		row_data.append(s)
		for t in alphabet:
			if t in set_states[s]:
				row_data.append(set_states[s][t])
			else:
				row_data.append("--")
			if len(row_data) == len(header):
				table.add_row(row_data)
	print(table)

def main():
	d_ndfa = read_data()
	result = to_dfa(d_ndfa['Initial_state'], d_ndfa, set_states = {})
	print_set_states(result)
	print_table(result, d_ndfa['Alphabet'])
	print_table(equivalence(result), d_ndfa['Alphabet'])

if __name__ == "__main__":
	main()